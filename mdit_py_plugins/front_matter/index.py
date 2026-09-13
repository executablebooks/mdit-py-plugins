"""Process front matter."""

from functools import partial

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock

from mdit_py_plugins.utils import is_code_block


def front_matter_plugin(md: MarkdownIt, *, marker: str = "-") -> None:
    """Plugin ported from
    `markdown-it-front-matter <https://github.com/ParkSB/markdown-it-front-matter>`__.

    It parses initial metadata, stored between opening/closing markers:

    .. code-block:: md

        ---
        valid-front-matter: true
        ---

    For example, to extract TOML-style front matter:

    .. code-block:: python

        md = MarkdownIt().use(front_matter_plugin, marker="+")
        tokens = md.parse('+++\\ntitle = "Hello"\\n+++\\n# Heading')
        assert tokens[0].content == 'title = "Hello"'

    :param marker: Single non-whitespace character used for the delimiters,
        excluding NUL (which Markdown normalizes before parsing).
        At least three repetitions are required; the closing delimiter must
        be at least as long as the opening delimiter. Defaults to ``-`` for
        YAML-style front matter. Use ``+`` for TOML-style ``+++`` delimiters
        or ``;`` for JSON-style ``;;;`` delimiters. The content is returned
        as raw text, without decoding YAML, TOML, or JSON. The YAML ``...``
        terminator is recognized only with the default marker.
    :raises ValueError: If the marker is not a single non-whitespace character,
        or is NUL.

    """
    if len(marker) != 1 or marker.isspace() or marker == "\x00":
        raise ValueError(
            "marker must be a single non-whitespace character other than NUL"
        )

    md.block.ruler.before(
        "table",
        "front_matter",
        partial(_front_matter_rule, marker_chr=marker),
        {"alt": ["paragraph", "reference", "blockquote", "list"]},
    )


def _front_matter_rule(
    state: StateBlock,
    startLine: int,
    endLine: int,
    silent: bool,
    *,
    marker_chr: str = "-",
) -> bool:
    min_markers = 3

    auto_closed = False
    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]
    src_len = len(state.src)

    # Check out the first character of the first line quickly,
    # this should filter out non-front matter
    if startLine != 0 or state.src[0] != marker_chr:
        return False

    # Check out the rest of the marker string
    # while pos <= 3
    pos = start + 1
    while pos <= maximum and pos < src_len:
        if state.src[pos] != marker_chr:
            break
        pos += 1

    marker_count = pos - start

    if marker_count < min_markers:
        return False

    # Since start is found, we can report success here in validation mode
    if silent:
        return True

    # Search for the end of the block
    nextLine = startLine

    while True:
        nextLine += 1
        if nextLine >= endLine:
            # unclosed block should be autoclosed by end of document.
            return False

        if marker_chr == "-" and state.src[start:maximum] == "...":
            break

        start = state.bMarks[nextLine] + state.tShift[nextLine]
        maximum = state.eMarks[nextLine]

        if start < maximum and state.sCount[nextLine] < state.blkIndent:
            # non-empty line with negative indent should stop the list:
            # - ```
            #  test
            break

        if state.src[start] != marker_chr:
            continue

        if is_code_block(state, nextLine):
            continue

        pos = start + 1
        while pos < maximum:
            if state.src[pos] != marker_chr:
                break
            pos += 1

        # closing code fence must be at least as long as the opening one
        if (pos - start) < marker_count:
            continue

        # make sure tail has spaces only
        pos = state.skipSpaces(pos)

        if pos < maximum:
            continue

        # found!
        auto_closed = True
        break

    old_parent = state.parentType
    old_line_max = state.lineMax
    state.parentType = "container"

    # this will prevent lazy continuations from ever going past our end marker
    state.lineMax = nextLine

    token = state.push("front_matter", "", 0)
    token.hidden = True
    token.markup = marker_chr * min_markers
    token.content = state.src[state.bMarks[startLine + 1] : state.eMarks[nextLine - 1]]
    token.block = True

    state.parentType = old_parent
    state.lineMax = old_line_max
    state.line = nextLine + (1 if auto_closed else 0)
    token.map = [startLine, state.line]

    return True
