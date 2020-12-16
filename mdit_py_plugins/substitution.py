from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline
from markdown_it.rules_block import StateBlock


def substitution_plugin(md: MarkdownIt):
    """A plugin to create substitution tokens.

    These, token should be handled by the renderer.

    Example::

        {{ block }}

        a {{ inline }} b

    """
    md.block.ruler.before("fence", "substitution_block", _substitution_block)
    md.inline.ruler.before("escape", "substitution_inline", _substitution_inline)


def _substitution_inline(state: StateInline, silent: bool):
    try:
        if (
            state.srcCharCode[state.pos] != 0x7B  # /* { */
            or state.srcCharCode[state.pos + 1] != 0x7B
        ):
            return False
    except IndexError:
        return False

    pos = state.pos + 2
    found_closing = False
    while True:
        try:
            end = state.srcCharCode.index(0x7D, pos)  # /* } */
        except ValueError:
            return False
        try:
            if state.srcCharCode[end + 1] == 0x7D:
                found_closing = True
                break
        except IndexError:
            return False
        pos = end + 2

    if not found_closing:
        return False

    text = state.src[state.pos + 2 : end].strip()
    state.pos = end + 2

    if silent:
        return True

    token = state.push("substitution_inline", "span", 0)
    token.block = False
    token.content = text
    token.attrSet("class", "substitution")
    token.attrSet("text", text)
    token.markup = "{{"

    return True


def _substitution_block(state: StateBlock, startLine: int, endLine: int, silent: bool):
    startPos = state.bMarks[startLine] + state.tShift[startLine]
    end = state.eMarks[startLine]

    # if it's indented more than 3 spaces, it should be a code block
    if state.sCount[startLine] - state.blkIndent >= 4:
        return False

    lineText = state.src[startPos:end].strip()

    try:
        if (
            lineText[0] != "{"
            or lineText[1] != "{"
            or lineText[-1] != "}"
            or lineText[-2] != "}"
            or len(lineText) < 5
        ):
            return False
    except IndexError:
        return False

    text = lineText[2:-2].strip()
    state.line = startLine + 1

    if silent:
        return True

    token = state.push("substitution_block", "div", 0)
    token.block = True
    token.content = text
    token.attrSet("class", "substitution")
    token.attrSet("text", text)
    token.markup = "{{"
    token.map = [startLine, state.line]

    return True
