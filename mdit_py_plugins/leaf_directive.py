from markdown_it import MarkdownIt
from markdown_it.common.utils import isSpace
from markdown_it.rules_block import StateBlock


def leaf_directive_plugin(md: MarkdownIt, parse_content: bool = True):
    """This plugin allows for a sinlge div to be created,
    with a single class and single paragraph.

    :param parse_content: Whether to parse the content of the div (as a paragraph)
        or simply store it as a string (for later processing).
    """

    def _rule(state: StateBlock, startLine: int, endLine: int, silent: bool):
        pos = state.bMarks[startLine] + state.tShift[startLine]
        maximum = state.eMarks[startLine]

        # if it's indented more than 3 spaces, it should be a code block
        if state.sCount[startLine] - state.blkIndent >= 4:
            return False

        if pos + 3 > maximum:
            return False

        #  Assert the line starts with `::`
        if state.srcCharCode[pos] != 0x3A or state.srcCharCode[pos + 1] != 0x3A:
            return False

        # But don't allow ``:::``, which is a div
        if state.srcCharCode[pos + 2] == 0x3A:
            return False

        # it must also not be whitespace
        if isSpace(state.srcCharCode[pos + 2]):
            return False

        if silent:
            return True

        # jump line-by-line until empty one or EOF
        nextLine = startLine + 1
        while nextLine < endLine:
            if state.isEmpty(nextLine):
                break
            nextLine += 1

        text = state.getLines(startLine, nextLine, state.blkIndent, False).strip()

        state.line = nextLine

        klass, *other = text[2:].split(maxsplit=1)
        content = other[0] if other else ""

        if parse_content:
            token = state.push("leaf_div_open", "div", 1)
            token.map = [startLine, state.line]
            token.markup = "::"
            token.attrSet("class", klass)

            if content:
                token = state.push("paragraph_open", "p", 1)
                token.map = [startLine, state.line]

                token = state.push("inline", "", 0)
                token.content = content
                token.map = [startLine, state.line]
                token.children = []

                token = state.push("paragraph_close", "p", -1)

            token = state.push("leaf_div_close", "div", -1)

        else:
            token = state.push("leaf_div", "div", 0)
            token.map = [startLine, state.line]
            token.markup = "::"
            token.attrSet("class", klass)
            token.content = content

        return True

    md.block.ruler.before(
        "fence",
        "leaf_directive",
        _rule,
    )
