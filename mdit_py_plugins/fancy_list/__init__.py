"""Fancy list plugin"""
import functools
import re
from typing import Dict, Literal, Tuple, Union

from markdown_it import MarkdownIt
from markdown_it.common.utils import isSpace
from markdown_it.rules_block import StateBlock
from markdown_it.token import Token
from roman import InvalidRomanNumeralError, fromRoman

# Ported from https://github.com/Moxio/markdown-it-fancy-lists

MarkerType = Literal["0", "a", "A", "i", "I", "#", "*", "-", "+"]


class Marker:
    isOrdered: bool
    isRoman: bool
    isAlpha: bool
    listType: MarkerType
    bulletChar: str
    hasOrdinalIndicator: bool
    delimiter: Literal[")", "."]
    start: int
    posAfterMarker: int
    original: str

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def __str__(self):
        return self.original


# Search `[-+*][\n ]`, returns next pos after marker on success
# or -1 on fail.
def parseUnorderedListMarker(state: StateBlock, startLine: int):
    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    marker = state.src[pos]
    pos += 1

    # Check bullet
    if marker not in "*-+":
        return None

    if pos < maximum:
        ch = state.srcCharCode[pos]

        if not isSpace(ch):
            # " -test " - is not a list item
            return None

    return {"listType": state.src[pos - 1], "posAfterMarker": pos, "original": marker}


# Search `^(\d{1,9}|[a-z]|[A-Z]|[ivxlcdm]+|[IVXLCDM]+|#)([\u00BA\u00B0\u02DA\u1D52]?)([.)])`,
# returns next pos after marker on success or -1 on fail.
def parseOrderedListMarker(state: StateBlock, startLine: int):
    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    # List marker should have at least 2 chars (digit + dot)
    if start + 1 >= maximum:
        return None

    stringContainingNumberAndMarker = state.src[start : min(maximum, start + 10)]

    match = re.match(
        "^(\\d{1,9}|[a-z]|[A-Z]|[ivxlcdm]+|[IVXLCDM]+|#)([\u00BA\u00B0\u02DA\u1D52]?)([.)])",
        stringContainingNumberAndMarker,
    )
    if not match:
        return None

    markerPos = start + len(match[1])
    markerChar = state.src[markerPos]

    finalPos = start + len(match[0])
    finalChar = state.srcCharCode[finalPos]

    #  requires once space after marker
    if not isSpace(finalChar):
        return None

    # requires two spaces after a capital letter and a period
    if (
        isCharCodeUppercaseAlpha(ord(match[1][0]))
        and len(match[1]) == 1
        and markerChar == "."
    ):
        finalPos += 1  # consume another space
        finalChar = state.srcCharCode[finalPos]
        if not isSpace(finalChar):
            return None

    return {
        "bulletChar": match[1],
        "hasOrdinalIndicator": match[2] != "",
        "delimiter": match[3],
        "posAfterMarker": finalPos,
        "original": match[0],
    }


def markTightParagraphs(state: StateBlock, idx: int):
    i: int = idx + 2
    l: int = len(state.tokens) - 2
    level = state.level + 2

    while i < l:
        if state.tokens[i].level == level and state.tokens[i].type == "paragraph_open":
            state.tokens[i + 2].hidden = True
            state.tokens[i].hidden = True
            i += 2
        i += 1


def isCharCodeDigit(charChode: int):
    return ord("0") <= charChode <= ord("9")


def isCharCodeLowercaseAlpha(charChode: int):
    return ord("a") <= charChode <= ord("z")


def isCharCodeUppercaseAlpha(charChode: int):
    return ord("A") <= charChode <= ord("Z")


def analyzeRoman(romanNumeralString: str):
    parsedRomanNumber: int = 1
    isValidRoman = True
    try:
        # This parser only works on uppercase letters (unlike the JS library.)
        parsedRomanNumber = fromRoman(romanNumeralString.upper())
    except InvalidRomanNumeralError:
        isValidRoman = False

    return (
        parsedRomanNumber,
        isValidRoman,
    )


def analyseMarker(
    state: StateBlock, startLine: int, endLine: int, previousMarker: Marker | None
):
    orderedListMarker = parseOrderedListMarker(state, startLine)
    if orderedListMarker is not None:
        bulletChar = orderedListMarker["bulletChar"]
        charCode = ord(orderedListMarker["bulletChar"][0])

        if isCharCodeDigit(charCode):
            return Marker(
                isOrdered=True,
                isRoman=False,
                isAlpha=False,
                listType="0",
                start=int(bulletChar),
                **orderedListMarker,
            )
        elif isCharCodeLowercaseAlpha(charCode):
            isValidAlpha = len(bulletChar) == 1
            preferRoman = (previousMarker is not None and previousMarker.isRoman) or (
                (previousMarker is None or not previousMarker.isAlpha)
                and bulletChar == "i"
            )
            parsedRomanNumber, isValidRoman = analyzeRoman(bulletChar)

            if isValidRoman and (not isValidAlpha or preferRoman):
                return Marker(
                    isOrdered=True,
                    isRoman=True,
                    isAlpha=False,
                    listType="i",
                    start=parsedRomanNumber,
                    **orderedListMarker,
                )
            elif isValidAlpha:
                return Marker(
                    isOrdered=True,
                    isRoman=False,
                    isAlpha=True,
                    listType="a",
                    start=ord(bulletChar) - ord("a") + 1,
                    **orderedListMarker,
                )
            return None
        elif isCharCodeUppercaseAlpha(charCode):
            isValidAlpha = len(bulletChar) == 1
            preferRoman = (previousMarker is not None and previousMarker.isRoman) or (
                (previousMarker is None or not previousMarker.isAlpha)
                and bulletChar == "I"
            )
            parsedRomanNumber, isValidRoman = analyzeRoman(bulletChar)

            if isValidRoman and (not isValidAlpha or preferRoman):
                return Marker(
                    isOrdered=True,
                    isRoman=True,
                    isAlpha=False,
                    listType="I",
                    start=parsedRomanNumber,
                    **orderedListMarker,
                )
            elif isValidAlpha:
                return Marker(
                    isOrdered=True,
                    isRoman=False,
                    isAlpha=True,
                    listType="A",
                    start=ord(bulletChar) - ord("A") + 1,
                    **orderedListMarker,
                )
            return None
        else:
            return Marker(
                isOrdered=True,
                isRoman=False,
                isAlpha=False,
                listType="#",
                start=1,
                **orderedListMarker,
            )
    unorderedListMarker = parseUnorderedListMarker(state, startLine)
    if unorderedListMarker:
        return Marker(
            isOrdered=False,
            isRoman=False,
            isAlpha=False,
            bulletChar="",
            hasOrdinalIndicator=False,
            delimiter=")",
            start=1,
            **unorderedListMarker,
        )
    return None


def areMarkersCompatible(previousMarker: Marker, currentMarker: Marker):
    return (
        previousMarker.isOrdered == currentMarker.isOrdered
        and (
            previousMarker.listType == currentMarker.listType
            or currentMarker.listType == "#"
        )
        and previousMarker.delimiter == currentMarker.delimiter
        and previousMarker.hasOrdinalIndicator == currentMarker.hasOrdinalIndicator
    )


def fancy_list_plugin(md: MarkdownIt, allow_ordinal: bool = False):
    """Fancy lists use the Pandoc rules to specify the style of ordered lists.

    .. code-block:: md

        1. One
            a. One
            b. Two
                i. One
                    A. One
                    B. Two
                        I.  One
                        II.  Two
                    C. Three
                ii. Two
            c. Three
        2. Two

    """
    md.block.ruler.at(
        "list",
        functools.partial(_fancylist_rule, allow_ordinal),
        {"alt": ["paragraph", "reference", "blockquote"]},
    )


def parseNameMarker(state: StateBlock, startLine: int) -> Tuple[int, str]:
    """Parse field name: `:name:`

    :returns: position after name marker, name text
    """
    start = state.bMarks[startLine] + state.tShift[startLine]
    pos = start
    maximum = state.eMarks[startLine]

    # marker should have at least 3 chars (colon + character + colon)
    if pos + 2 >= maximum:
        return -1, ""

    # first character should be ':'
    if state.src[pos] != ":":
        return -1, ""

    # scan name length
    name_length = 1
    found_close = False
    for ch in state.src[pos + 1 :]:
        if ch == "\n":
            break
        if ch == ":":
            # TODO backslash escapes
            found_close = True
            break
        name_length += 1

    if not found_close:
        return -1, ""

    # get name
    name_text = state.src[pos + 1 : pos + name_length]

    # name should contain at least one character
    if not name_text.strip():
        return -1, ""

    return pos + name_length + 1, name_text


def _fancylist_rule(
    allowOrdinal: bool, state: StateBlock, startLine: int, endLine: int, silent: bool
):
    # if it's indented more than 3 spaces, it should be a code block
    if state.sCount[startLine] - state.blkIndent >= 4:
        return False

    # Special case:
    #  - item 1
    #   - item 2
    #    - item 3
    #     - item 4
    #      - this one is a paragraph continuation
    if (
        state.listIndent >= 0
        and state.sCount[startLine] - state.listIndent >= 4
        and state.sCount[startLine] < state.blkIndent
    ):
        return False

    isTerminatingParagraph = False
    # limit conditions when list can interrupt
    # a paragraph (validation mode only)
    if silent and state.parentType == "paragraph":
        # Next list item should still terminate previous list item;
        #
        # This code can fail if plugins use blkIndent as well as lists,
        # but I hope the spec gets fixed long before that happens.
        #
        if state.tShift[startLine] >= state.blkIndent:
            isTerminatingParagraph = True

    marker: Marker = analyseMarker(state, startLine, endLine, None)
    if marker is None:
        return False

    if marker.hasOrdinalIndicator and not allowOrdinal:
        return False

    # do not allow subsequent numbers to interrupt paragraphs in non-nested lists
    isNestedList = state.listIndent != -1
    if isTerminatingParagraph and marker.start != 1 and not isNestedList:
        return False

    # If we're starting a new unordered list right after
    # a paragraph, first line should not be empty.
    if isTerminatingParagraph:
        if state.skipSpaces(marker.posAfterMarker) >= state.eMarks[startLine]:
            return False

    # We should terminate list on style change. Remember first one to compare.
    markerCharCode = ord(state.src[marker.posAfterMarker - 1])

    # For validation mode we can terminate immediately
    if silent:
        return True

    # Start list
    listTokIdx = len(state.tokens)

    token: Token
    if marker.isOrdered:
        token = state.push("ordered_list_open", "ol", 1)
        attrs: Dict[str, Union[str, int, float]] = {}
        if marker.listType != "0" and marker.listType != "#":
            attrs["type"] = str(marker.listType)
        if marker.start != 1:
            attrs["start"] = str(marker.start)
        if marker.hasOrdinalIndicator:
            attrs["class"] = "ordinal"
        token.attrs = attrs
    else:
        token = state.push("bullet_list_open", "ul", 1)

    listLines = [startLine, 0]
    token.map = listLines
    token.markup = chr(markerCharCode)

    #
    # Iterate list items
    #

    nextLine = startLine
    prevEmptyEnd = False
    terminatorRules = state.md.block.ruler.getRules("list")

    oldParentType = state.parentType
    state.parentType = "list"

    tight = True
    while nextLine < endLine:
        nextMarker = analyseMarker(state, nextLine, endLine, marker)
        if nextMarker is None or not areMarkersCompatible(marker, nextMarker):
            break
        pos: int = nextMarker.posAfterMarker
        maximum = state.eMarks[nextLine]

        initial = offset = (
            state.sCount[nextLine]
            + pos
            - (state.bMarks[startLine] + state.tShift[startLine])
        )

        while pos < maximum:
            ch = state.srcCharCode[pos]

            if ch == 0x09:
                offset += 4 - (offset + state.bsCount[nextLine]) % 4
            elif ch == 0x20:
                offset += 1
            else:
                break

            pos += 1

        contentStart = pos

        indentAfterMarker: int = 1
        if contentStart >= maximum:
            # trimming space in "-    \n  3" case, indent is 1 here
            indentAfterMarker = 1
        else:
            indentAfterMarker = offset - initial

        # If we have more than 4 spaces, the indent is 1
        # (the rest is just indented code block)
        if indentAfterMarker > 4:
            indentAfterMarker = 1

        # "  -  test"
        #  ^^^^^ - calculating total length of this thing
        indent = initial + indentAfterMarker

        # Run subparser & write tokens
        token = state.push("list_item_open", "li", 1)
        token.markup = chr(markerCharCode)
        token.map = itemLines = [int(startLine), 0]

        # change current state, then restore it after parser subcall
        oldTight = state.tight
        oldTShift = state.tShift[startLine]
        oldSCount = state.sCount[startLine]

        #  - example list
        # ^ listIndent position will be here
        #   ^ blkIndent position will be here
        #
        oldListIndent = state.listIndent
        state.listIndent = state.blkIndent
        state.blkIndent = indent

        state.tight = True
        state.tShift[startLine] = contentStart - state.bMarks[startLine]
        state.sCount[startLine] = offset

        if contentStart >= maximum and state.isEmpty(startLine + 1):
            # workaround for this case
            # (list item is empty, list terminates before "foo"):
            # ~~~~~~~~
            #   -
            #
            #     foo
            # ~~~~~~~~
            state.line = min(state.line + 2, endLine)
        else:
            state.md.block.tokenize(state, startLine, endLine)

        # If any of list item is tight, mark list as tight
        if not state.tight or prevEmptyEnd:
            tight = False
        # Item become loose if finish with empty line,
        # but we should filter last element, because it means list finish
        prevEmptyEnd = (state.line - startLine) > 1 and state.isEmpty(state.line - 1)

        state.blkIndent = state.listIndent
        state.listIndent = oldListIndent
        state.tShift[startLine] = oldTShift
        state.sCount[startLine] = oldSCount
        state.tight = oldTight

        token = state.push("list_item_close", "li", -1)
        token.markup = chr(markerCharCode)

        nextLine = startLine = state.line
        itemLines[1] = nextLine
        contentStart = state.bMarks[startLine]

        if nextLine >= endLine:
            break

        #
        # Try to check if list is terminated or continued.
        #
        if state.sCount[nextLine] < state.blkIndent:
            break

        # if it's indented more than 3 spaces, it should be a code block
        if state.sCount[startLine] - state.blkIndent >= 4:
            break

        # fail if terminating block found
        terminate = False
        for rule in terminatorRules:
            if rule(state, nextLine, endLine, True):
                terminate = True
                break
        if terminate:
            break

        marker = nextMarker

    # Finalize list
    if marker.isOrdered:
        token = state.push("ordered_list_close", "ol", -1)
    else:
        token = state.push("bullet_list_close", "ul", -1)

    token.markup = chr(markerCharCode)

    listLines[1] = nextLine
    state.line = nextLine

    state.parentType = oldParentType

    # mark paragraphs tight if needed
    if tight:
        markTightParagraphs(state, listTokIdx)

    return True
