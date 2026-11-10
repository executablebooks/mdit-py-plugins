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

    A reference is a ``§`` immediately followed by ASCII digits, optionally
    grouped into further ``.``-separated levels (no spaces are allowed).
    A trailing dot is not consumed, so ``see §1.`` captures ``§1``.  A ``§``
    directly followed by an ASCII letter (e.g. ``§1a``) is *not* a reference,
    but a following non-ASCII letter does not block a match, so ``见§3章``
    still captures ``§3``.  A reference with any level longer than nine
    digits (e.g. ``§1.1234567890``) is not a reference either: the whole
    text stays literal, rather than a shorter prefix being captured.
    Leading zeros count towards the nine digits, so ``§0000000001`` stays
    literal too.
    Following CommonMark backslash-escape behaviour, ``\\§1`` stays literal
    text, while ``\\\\§1`` renders a literal backslash followed by a live
    reference.

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
