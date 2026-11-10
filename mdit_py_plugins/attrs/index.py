from __future__ import annotations

from collections.abc import Sequence
from functools import partial
import re
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.rules_core import StateCore
from markdown_it.rules_inline import StateInline
from markdown_it.token import Token

from mdit_py_plugins.utils import is_code_block

from .parse import ParseError, parse


def attrs_plugin(
    md: MarkdownIt,
    *,
    after: Sequence[str] = ("image", "code_inline", "link_close", "span_close"),
    spans: bool = False,
    span_after: str = "link",
    allowed: Sequence[str] | None = None,
) -> None:
    """Parse inline attributes that immediately follow certain inline elements::

        ![alt](https://image.com){#id .a b=c}

    This syntax is inspired by
    `Djot spans
    <https://htmlpreview.github.io/?https://github.com/jgm/djot/blob/master/doc/syntax.html#inline-attributes>`_.

    Inside the curly braces, the following syntax is possible:

    - `.foo` specifies foo as a class.
      Multiple classes may be given in this way; they will be combined.
    - `#foo` specifies foo as an identifier.
      An element may have only one identifier;
      if multiple identifiers are given, the last one is used.
    - `key="value"` or `key=value` specifies a key-value attribute.
       Quotes are not needed when the value consists entirely of
       ASCII alphanumeric characters or `_` or `:` or `-`.
       Backslash escapes may be used inside quoted values,
       to allow a ``"`` character within the value.
       Note that the backslash is retained in the value:
       ``{k="a\\"b"}`` gives ``k`` the value ``a\\"b``.
    - `%` begins a comment, which ends with the next `%`.
      If no further `%` occurs in the rest of the line (for a block attribute)
      or of the inline content (for an inline attribute),
      the comment instead ends at the next `}`, which also ends the attribute.

    Multiple attribute blocks are merged.

    :param md: The MarkdownIt instance to modify.
    :param after: The names of inline elements after which attributes may be specified.
        This plugin does not support attributes after emphasis, strikethrough or text elements,
        which all require post-parse processing.
    :param spans: If True, also parse attributes after spans of text, encapsulated by `[]`.
        Note Markdown link references take precedence over this syntax.
    :param span_after: The name of an inline rule after which spans may be specified.
    :param allowed: A list of allowed attribute names.
        If not ``None``, any attributes not in this list will be removed
        and placed in the token's meta under the key "insecure_attrs".
        If ``None`` (the default), event-handler attributes
        (any name starting with ``on``, such as ``onclick``) are still removed,
        as a baseline protection against script injection.
        Other attributes, including ``style``, are kept.
        Whatever ``allowed`` says, the URL-valued attributes
        ``href``, ``src``, ``action``, ``formaction`` and ``xlink:href``
        are removed when ``md.validateLink`` rejects their value
        (for example a ``javascript:`` URL), as for Markdown links and images.
        This is not a full sanitiser: to safely render untrusted input,
        pass an explicit ``allowed`` list (e.g. ``("id", "class")``).
    """

    if spans:
        md.inline.ruler.after(
            span_after,
            "span",
            partial(_span_rule, allowed=None if allowed is None else set(allowed)),
        )
    if after:
        md.inline.ruler.push(
            "attr",
            partial(
                _attr_inline_rule,
                after=after,
                allowed=None if allowed is None else set(allowed),
            ),
        )


def attrs_block_plugin(md: MarkdownIt, *, allowed: Sequence[str] | None = None) -> None:
    """Parse block attributes.

    Block attributes are attributes on a single line, with no other content.
    They attach the specified attributes to the block below them::

        {.a #b c=1}
        A paragraph, that will be assigned the class ``a`` and the identifier ``b``.

    Attributes can be stacked, with classes accumulating and lower attributes overriding higher::

        {#a .a c=1}
        {#b .b c=2}
        A paragraph, that will be assigned the class ``a b c``, and the identifier ``b``.

    This syntax is inspired by Djot block attributes.

    :param allowed: A list of allowed attribute names.
        If not ``None``, any attributes not in this list will be removed
        and placed in the token's meta under the key "insecure_attrs".
        If ``None`` (the default), event-handler attributes
        (any name starting with ``on``, such as ``onclick``) are still removed,
        as a baseline protection against script injection.
        Other attributes, including ``style``, are kept.
        Whatever ``allowed`` says, the URL-valued attributes
        ``href``, ``src``, ``action``, ``formaction`` and ``xlink:href``
        are removed when ``md.validateLink`` rejects their value
        (for example a ``javascript:`` URL), as for Markdown links and images.
        This is not a full sanitiser: to safely render untrusted input,
        pass an explicit ``allowed`` list (e.g. ``("id", "class")``).
    """
    md.block.ruler.before("fence", "attr", _attr_block_rule)
    md.core.ruler.after(
        "block",
        "attr",
        partial(
            _attr_resolve_block_rule, allowed=None if allowed is None else set(allowed)
        ),
    )


def _find_opening(tokens: Sequence[Token], index: int) -> int | None:
    """Find the opening token index, if the token is closing."""
    if tokens[index].nesting != -1:
        return index
    level = 0
    while index >= 0:
        level += tokens[index].nesting
        if level == 0:
            return index
        index -= 1
    return None


def _span_rule(
    state: StateInline, silent: bool, *, allowed: set[str] | None = None
) -> bool:
    if state.src[state.pos] != "[":
        return False

    maximum = state.posMax
    labelStart = state.pos + 1
    labelEnd = state.md.helpers.parseLinkLabel(state, state.pos, False)

    # parser failed to find ']', so it's not a valid span
    if labelEnd < 0:
        return False

    pos = labelEnd + 1

    # check not at end of inline
    if pos >= maximum:
        return False

    try:
        new_pos, attrs = parse(state.src[pos:])
    except ParseError:
        return False

    pos += new_pos + 1

    if not silent:
        state.pos = labelStart
        state.posMax = labelEnd
        token = state.push("span_open", "span", 1)
        _add_attrs(state.md, token, attrs, allowed)
        state.md.inline.tokenize(state)
        token = state.push("span_close", "span", -1)

    state.pos = pos
    state.posMax = maximum
    return True


def _attr_inline_rule(
    state: StateInline,
    silent: bool,
    after: Sequence[str],
    *,
    allowed: set[str] | None = None,
) -> bool:
    if state.pending or not state.tokens:
        return False
    token = state.tokens[-1]
    if token.type not in after:
        return False
    try:
        new_pos, attrs = parse(state.src[state.pos :])
    except ParseError:
        return False
    token_index = _find_opening(state.tokens, len(state.tokens) - 1)
    if token_index is None:
        return False
    state.pos += new_pos + 1
    if not silent:
        attr_token = state.tokens[token_index]
        if "class" in attrs and "class" in attr_token.attrs:
            attrs["class"] = f"{attr_token.attrs['class']} {attrs['class']}"
        _add_attrs(state.md, attr_token, attrs, allowed)
    return True


def _attr_block_rule(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    """Find a block of attributes.

    The block must be a single line that begins with a `{`, after three or less spaces,
    and end with a `}` followed by any number if spaces.
    """
    if is_code_block(state, startLine):
        return False

    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    # if it doesn't start with a {, it's not an attribute block
    if state.src[pos] != "{":
        return False

    # find first non-space character from the right
    while maximum > pos and state.src[maximum - 1] in (" ", "\t"):
        maximum -= 1
    # if it doesn't end with a }, it's not an attribute block
    if maximum <= pos:
        return False
    if state.src[maximum - 1] != "}":
        return False

    try:
        _new_pos, attrs = parse(state.src[pos:maximum])
    except ParseError:
        return False

    # if the block was resolved earlier than expected, it's not an attribute block
    # TODO this was not working in some instances, so I disabled it
    # if (maximum - 1) != new_pos:
    #     return False

    if silent:
        return True

    token = state.push("attrs_block", "", 0)
    token.attrs = attrs  # type: ignore[assignment]
    token.map = [startLine, startLine + 1]

    state.line = startLine + 1
    return True


def _attr_resolve_block_rule(state: StateCore, *, allowed: set[str] | None) -> None:
    """Find attribute block then move its attributes to the next block."""
    i = 0
    len_tokens = len(state.tokens)
    while i < len_tokens:
        if state.tokens[i].type != "attrs_block":
            i += 1
            continue

        # skip closing tokens; attributes would be rendered into the closing tag
        if i + 1 < len_tokens and state.tokens[i + 1].nesting >= 0:
            next_token = state.tokens[i + 1]

            # classes are appended
            if "class" in state.tokens[i].attrs and "class" in next_token.attrs:
                state.tokens[i].attrs["class"] = (
                    f"{state.tokens[i].attrs['class']} {next_token.attrs['class']}"
                )

            if next_token.type == "attrs_block":
                # subsequent attribute blocks take precedence, when merging
                for key, value in state.tokens[i].attrs.items():
                    if key == "class" or key not in next_token.attrs:
                        next_token.attrs[key] = value
            else:
                _add_attrs(state.md, next_token, state.tokens[i].attrs, allowed)

        state.tokens.pop(i)
        len_tokens -= 1


_URL_ATTRS = frozenset(("href", "src", "action", "formaction", "xlink:href"))
"""Attributes whose value is a URL, checked with ``md.validateLink``."""

_URL_IGNORED_RE = re.compile(r"[\t\n\r]")
_URL_STRIP = "".join(chr(i) for i in range(0x21))


def _is_insecure_attr(key: str) -> bool:
    """Return True for event-handler attributes (``on*``, e.g. ``onclick``).

    They execute JavaScript, so they are removed by default
    when no explicit ``allowed`` list is given.
    """
    return key.lower().startswith("on")


def _is_valid_url(md: MarkdownIt, value: Any) -> bool:
    """Return True if ``md.validateLink`` accepts a URL-valued attribute.

    Browsers ignore ASCII tabs and newlines anywhere in a URL,
    and control characters and spaces around it, before reading its scheme
    (so ``java<TAB>script:`` is a ``javascript:`` URL).
    The value is emitted as written, so those characters are removed
    before it is normalised and validated.
    """
    url = _URL_IGNORED_RE.sub("", str(value)).strip(_URL_STRIP)
    return md.validateLink(md.normalizeLink(url))


def _add_attrs(
    md: MarkdownIt,
    token: Token,
    attrs: dict[str, Any],
    allowed: set[str] | None,
) -> None:
    """Add attributes to a token, skipping any disallowed attributes.

    When ``allowed`` is not ``None`` only those names are kept.
    When it is ``None`` (the default) event-handler (``on*``) attributes
    are still removed, so untrusted input cannot inject script.
    In both cases, a URL-valued attribute (``href``, ``src``, ...)
    is removed if ``md.validateLink`` rejects it.
    Anything removed is preserved in ``token.meta["insecure_attrs"]``.
    """
    if allowed is not None:
        disallowed = {k: v for k, v in attrs.items() if k not in allowed}
    else:
        disallowed = {k: v for k, v in attrs.items() if _is_insecure_attr(k)}
    disallowed.update(
        (k, v)
        for k, v in attrs.items()
        if k not in disallowed and k.lower() in _URL_ATTRS and not _is_valid_url(md, v)
    )

    if disallowed:
        token.meta["insecure_attrs"] = disallowed
        attrs = {k: v for k, v in attrs.items() if k not in disallowed}

    # attributes takes precedence over existing attributes
    token.attrs.update(attrs)
