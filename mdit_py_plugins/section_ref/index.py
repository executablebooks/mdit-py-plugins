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


def section_ref_plugin(md: MarkdownIt) -> None:
    """Parse section-sign references such as ``§1``, ``§1.1`` and ``§2.3.4``.

    A reference is a ``§`` immediately followed by ASCII digits, optionally
    grouped into further ``.``-separated levels (no spaces are allowed).
    A trailing dot is not consumed, so ``see §1.`` captures ``§1``.  A ``§``
    directly followed by an ASCII letter (e.g. ``§1a``) is *not* a reference,
    but a following non-ASCII letter does not block a match, so ``见§3章``
    still captures ``§3``.  Following CommonMark backslash-escape behaviour,
    ``\\§1`` stays literal text, while ``\\\\§1`` renders a literal backslash
    followed by a live reference.

    Each reference becomes a ``section_ref`` token, with the matched text
    (e.g. ``"§1.1"``) as its ``content``, ``markup`` set to ``§`` and
    ``meta["numbers"]`` holding the parsed section number as a list of ints
    (e.g. ``[1, 1]`` for ``§1.1``), so that downstream renderers can resolve
    it to a heading target without re-parsing.  Leading zeros are normalized
    (``§01.02`` gives ``[1, 2]``); the original text remains in ``content``.

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

    if not silent:
        token = state.push("section_ref", "", 0)
        token.content = match.group(0)
        token.markup = "§"
        token.meta = {"numbers": [int(part) for part in match.group(1).split(".")]}

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
