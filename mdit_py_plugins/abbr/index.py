# Enclose abbreviations in <abbr> tags
#

import re
from typing import List

from markdown_it import MarkdownIt
from markdown_it.common.utils import arrayReplaceAt, escapeRE
from markdown_it.rules_block import StateBlock
from markdown_it.token import Token

# ASCII characters in Cc, Sc, Sm, Sk categories we should terminate on;
# you can check character classes here:
# http://www.unicode.org/Public/UNIDATA/UnicodeData.txt
OTHER_CHARS = r" \r\n$+<=>^`|~"

UNICODE_PUNCT_RE = r"[!-#%-\*,-\/:;\?@\[-\]_\{\}\xA1\xA7\xAB\xB6\xB7\xBB\xBF\u037E\u0387\u055A-\u055F\u0589\u058A\u05BE\u05C0\u05C3\u05C6\u05F3\u05F4\u0609\u060A\u060C\u060D\u061B\u061E\u061F\u066A-\u066D\u06D4\u0700-\u070D\u07F7-\u07F9\u0830-\u083E\u085E\u0964\u0965\u0970\u09FD\u0A76\u0AF0\u0C84\u0DF4\u0E4F\u0E5A\u0E5B\u0F04-\u0F12\u0F14\u0F3A-\u0F3D\u0F85\u0FD0-\u0FD4\u0FD9\u0FDA\u104A-\u104F\u10FB\u1360-\u1368\u1400\u166D\u166E\u169B\u169C\u16EB-\u16ED\u1735\u1736\u17D4-\u17D6\u17D8-\u17DA\u1800-\u180A\u1944\u1945\u1A1E\u1A1F\u1AA0-\u1AA6\u1AA8-\u1AAD\u1B5A-\u1B60\u1BFC-\u1BFF\u1C3B-\u1C3F\u1C7E\u1C7F\u1CC0-\u1CC7\u1CD3\u2010-\u2027\u2030-\u2043\u2045-\u2051\u2053-\u205E\u207D\u207E\u208D\u208E\u2308-\u230B\u2329\u232A\u2768-\u2775\u27C5\u27C6\u27E6-\u27EF\u2983-\u2998\u29D8-\u29DB\u29FC\u29FD\u2CF9-\u2CFC\u2CFE\u2CFF\u2D70\u2E00-\u2E2E\u2E30-\u2E4E\u3001-\u3003\u3008-\u3011\u3014-\u301F\u3030\u303D\u30A0\u30FB\uA4FE\uA4FF\uA60D-\uA60F\uA673\uA67E\uA6F2-\uA6F7\uA874-\uA877\uA8CE\uA8CF\uA8F8-\uA8FA\uA8FC\uA92E\uA92F\uA95F\uA9C1-\uA9CD\uA9DE\uA9DF\uAA5C-\uAA5F\uAADE\uAADF\uAAF0\uAAF1\uABEB\uFD3E\uFD3F\uFE10-\uFE19\uFE30-\uFE52\uFE54-\uFE61\uFE63\uFE68\uFE6A\uFE6B\uFF01-\uFF03\uFF05-\uFF0A\uFF0C-\uFF0F\uFF1A\uFF1B\uFF1F\uFF20\uFF3B-\uFF3D\uFF3F\uFF5B\uFF5D\uFF5F-\uFF65]|\uD800[\uDD00-\uDD02\uDF9F\uDFD0]|\uD801\uDD6F|\uD802[\uDC57\uDD1F\uDD3F\uDE50-\uDE58\uDE7F\uDEF0-\uDEF6\uDF39-\uDF3F\uDF99-\uDF9C]|\uD803[\uDF55-\uDF59]|\uD804[\uDC47-\uDC4D\uDCBB\uDCBC\uDCBE-\uDCC1\uDD40-\uDD43\uDD74\uDD75\uDDC5-\uDDC8\uDDCD\uDDDB\uDDDD-\uDDDF\uDE38-\uDE3D\uDEA9]|\uD805[\uDC4B-\uDC4F\uDC5B\uDC5D\uDCC6\uDDC1-\uDDD7\uDE41-\uDE43\uDE60-\uDE6C\uDF3C-\uDF3E]|\uD806[\uDC3B\uDE3F-\uDE46\uDE9A-\uDE9C\uDE9E-\uDEA2]|\uD807[\uDC41-\uDC45\uDC70\uDC71\uDEF7\uDEF8]|\uD809[\uDC70-\uDC74]|\uD81A[\uDE6E\uDE6F\uDEF5\uDF37-\uDF3B\uDF44]|\uD81B[\uDE97-\uDE9A]|\uD82F\uDC9F|\uD836[\uDE87-\uDE8B]|\uD83A[\uDD5E\uDD5F]"  # noqa: E501
UNICODE_SPACE_RE = r"[ \xA0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]"


def abbr_plugin(md: MarkdownIt):
    """Plugin ported from
    `markdown-it-abbr <https://github.com/markdown-it/markdown-it-abbr>`__.

    .. code-block:: md

            *[HTML]: HyperText Markup Language
    """

    md.block.ruler.before(
        "reference", "abbr_def", abbr_def, {"alt": ["paragraph", "reference"]}
    )
    md.core.ruler.after("linkify", "abbr_replace", abbr_replace)


# ## RULES ##


def abbr_def(state: StateBlock, startLine: int, endLine: int, silent: bool):
    pos = state.bMarks[startLine] + state.tShift[startLine]
    max = state.eMarks[startLine]

    if (pos + 2) >= max:
        return False

    if state.srcCharCode[pos] != 0x2A:  # /* * */
        return False
    pos += 1
    if state.srcCharCode[pos] != 0x5B:  # /* [ */
        return False
    pos += 1

    labelStart = pos
    labelEnd = None

    while pos < max:
        ch = state.srcCharCode[pos]
        if ch == 0x5B:  # /* [ */
            return False
        elif ch == 0x5D:  # /* ] */
            labelEnd = pos
            break
        elif ch == 0x5C:  # /* \ */
            pos += 1
        pos += 1

    if labelEnd is None or state.srcCharCode[labelEnd + 1] != 0x3A:
        return False

    if silent:
        return True

    label = state.src[labelStart:labelEnd].replace("\\\\", "")
    title = state.src[labelEnd + 2 : max].strip()

    if len(label) == 0:
        return False
    if len(title) == 0:
        return False
    if "abbreviations" not in state.env:
        state.env["abbreviations"] = {}
    if (":" + label) not in state.env["abbreviations"]:
        state.env["abbreviations"][":" + label] = title

    state.line = startLine + 1
    return True


def abbr_replace(state: StateBlock):
    if "abbreviations" not in state.env:
        return

    alternations = "|".join(
        map(
            escapeRE,
            reversed(
                sorted([key[1:] for key in state.env["abbreviations"].keys()], key=len)
            ),
        )
    )

    regSimple = re.compile(f"(?:{alternations})")

    otherChars = "".join([escapeRE(ch) for ch in OTHER_CHARS])

    regText = f"(^|{UNICODE_PUNCT_RE}|{UNICODE_SPACE_RE}|[{otherChars}])({alternations})($|{UNICODE_PUNCT_RE}|{UNICODE_SPACE_RE}|[{otherChars}])"  # noqa E501

    reg = re.compile(regText)

    blockTokens = state.tokens

    for j in range(len(blockTokens)):
        if blockTokens[j].type != "inline":
            continue
        tokens = blockTokens[j].children

        # we scan from the end, to keep position when new tags added
        assert tokens is not None
        i = len(tokens)
        while i >= 1:
            i -= 1
            assert isinstance(tokens, list)
            currentToken = tokens[i]

            if currentToken.type != "text":
                continue

            pos = 0
            lastIndex = 0
            text = currentToken.content
            nodes: List[Token] = []

            # fast regexp run to determine whether there are any abbreviated
            # words in the current token
            if regSimple.search(text) is None:
                continue

            while lastIndex < len(text):
                match = reg.search(text, lastIndex)
                if match is None:
                    break

                if match.start() > 0 or len(match.group(1)) > 0:
                    token = Token("text", "", 0)
                    token.content = text[pos : match.start() + len(match.group(1))]
                    nodes.append(token)

                token = Token("abbr_open", "abbr", 1)
                token.attrSet("title", state.env["abbreviations"][":" + match.group(2)])
                nodes.append(token)

                token = Token("text", "", 0)
                token.content = match.group(2)
                nodes.append(token)

                token = Token("abbr_close", "abbr", -1)
                nodes.append(token)

                lastIndex = match.start() + len(match.group(0)) - len(match.group(3))
                pos = lastIndex

            if len(nodes) == 0:
                continue

            if pos < len(text):
                token = Token("text", "", 0)
                token.content = text[pos:]
                nodes.append(token)

            # replace current node
            blockTokens[j].children = tokens = arrayReplaceAt(tokens, i, nodes)
