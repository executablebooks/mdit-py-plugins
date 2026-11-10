"""Section reference inline rule.

A single inline scanner is registered on the character ``§``:

- **section_ref** (char ``§``): section-sign references like ``§1.2``.

``§`` is *not* one of markdown-it-py's default text-rule terminator
characters, so the text rule would otherwise swallow it mid-paragraph and
the inline rule would never fire.  ``add_terminator_char("§")`` makes the
text rule interrupt at every ``§``, giving this rule a chance to run.  That
API is only available in markdown-it-py >= 4.1.0.

Requires markdown-it-py >= 4.1.0.
"""

from collections.abc import Sequence
import re
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.rules_inline import StateInline

if TYPE_CHECKING:
    from markdown_it.renderer import RendererProtocol
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict

# ASCII digits only (``[0-9]``, never ``\d`` which also matches unicode digits).
_SECTION_REF_PATTERN = re.compile(r"§([0-9]+(?:\.[0-9]+)*)")

# Longest dotted part (in written digits, leading zeros included) that is still
# read as a section number.  Nine digits keeps every number below 10**9, so it
# fits a signed 32-bit integer for downstream consumers, and keeps ``int()`` far
# below Python's integer string conversion limit (4300 digits by default, and
# never configurable below 640), which would otherwise raise ``ValueError`` and
# abort the whole render.  No real document has a billion sections.
_MAX_PART_DIGITS = 9


def section_ref_plugin(md: MarkdownIt) -> None:
    """Parse section-sign references such as ``§1``, ``§1.1`` and ``§2.3.4``.

    The grammar is normative:

    - A reference is ``§`` (U+00A7) immediately followed by one or more
      ``.``-separated levels, with no spaces.
      Each level is 1 to 9 ASCII digits, ``§([0-9]{1,9}(\\.[0-9]{1,9})*)``,
      and the match is maximal.
      Only ASCII ``0``-``9`` are digits: other Unicode digits, such as
      Arabic-Indic (U+0660 to U+0669) or fullwidth (U+FF10 to U+FF19) digits,
      do not form a reference, so a ``§`` followed by one stays literal text.
    - A trailing ``.`` is not part of the reference,
      so in ``see §1.`` the reference is ``§1`` and the ``.`` stays text.
    - There is no reference, and the whole run stays literal text,
      if the character after the match is an ASCII letter (``§1a``, ``§1.2b``),
      or if any level has more than nine digits, counting leading zeros
      (``§1234567890``, ``§0000000001``).
      No shorter prefix is taken, so ``§1.1234567890.2`` stays literal too.
      A non-ASCII letter after the match does not block it,
      so ``见§3章`` captures ``§3``.
    - References are recognised wherever inline text is parsed,
      and not inside code spans, autolinks, inline math or raw HTML tags
      (an attribute value is not inline text, but the text between two tags is,
      so ``<span title="§1">§2</span>`` captures ``§2`` only).
    - ``\\§`` is not a CommonMark backslash escape,
      because ``§`` is not ASCII punctuation:
      in ``\\§1`` the backslash stays visible and no reference is formed.
      ``\\\\§1`` is a literal backslash followed by the reference ``§1``.
      To write a literal sign, use ``&sect;`` or ``&#167;``,
      which never form a reference (``&sect;1`` renders as the text ``§1``).

    Each reference becomes a single ``section_ref`` leaf token
    (``nesting=0``, ``children=None``, ``tag=""``, ``attrs={}``),
    with ``markup`` set to ``"§"``, the text as written (e.g. ``"§01.02"``)
    as its ``content``, and ``meta["numbers"]`` holding the integer value of
    each level as a list of ints (``[1, 2]`` for ``§01.02``; every value is at
    most 999,999,999), so that downstream renderers can resolve it to a
    heading target without re-parsing.
    The token shape is part of the public API from 0.7.0.

    The default rendering is ``<span class="section-ref">§1.1</span>``.
    Override it with ``md.add_render_rule("section_ref", ...)``.
    markdown-it-py's ``renderInlineAsText``, which renders image ``alt`` text,
    keeps only ``text`` tokens, so ``![a §7 b](x.png)`` renders ``alt="a  b"``
    (as it does for inline math). A renderer that wants the reference in the
    alt text should use the ``section_ref`` token's ``content``.

    .. versionadded:: 0.7.0

    Requires markdown-it-py >= 4.1.0.
    """
    if not hasattr(md.inline, "add_terminator_char"):
        raise RuntimeError("section_ref_plugin requires markdown-it-py >= 4.1.0")

    md.inline.add_terminator_char("§")
    md.inline.ruler.push("section_ref", _section_ref_rule)
    md.add_render_rule("section_ref", render_section_ref)


def _section_ref_rule(state: StateInline, silent: bool) -> bool:
    match = _SECTION_REF_PATTERN.match(state.src, state.pos, state.posMax)
    if not match:
        return False

    # reject when directly followed by an ASCII letter (e.g. "§1a", "§1.2b"),
    # which indicates the text is not a plain section-number reference
    # (a following non-ASCII letter such as CJK must not block the match)
    end = match.end()
    if end < state.posMax and state.src[end].isascii() and state.src[end].isalpha():
        return False

    # reject an over-long level outright, so hostile input can never raise in
    # ``int()``; the whole text stays literal (no prefix match splits a number)
    parts = match.group(1).split(".")
    if any(len(part) > _MAX_PART_DIGITS for part in parts):
        return False

    if not silent:
        token = state.push("section_ref", "", 0)
        token.content = match.group(0)
        token.markup = "§"
        token.meta = {"numbers": [int(part) for part in parts]}

    state.pos = end
    return True


def render_section_ref(
    self: "RendererProtocol",
    tokens: Sequence["Token"],
    idx: int,
    options: "OptionsDict",
    env: "EnvType",
) -> str:
    token = tokens[idx]
    return f'<span class="section-ref">{escapeHtml(token.content)}</span>'
