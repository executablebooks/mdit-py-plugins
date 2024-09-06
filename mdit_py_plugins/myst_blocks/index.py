from __future__ import annotations

from functools import partial
import itertools
from typing import TYPE_CHECKING, Sequence

from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from markdown_it.rules_block import StateBlock

from mdit_py_plugins.utils import is_code_block

if TYPE_CHECKING:
    from markdown_it.renderer import RendererProtocol
    from markdown_it.token import Token
    from markdown_it.utils import EnvType, OptionsDict


def myst_block_plugin(md: MarkdownIt, *, single_line_directives=False, sld_markers: str = "`") -> None:
    """Parse MyST targets (``(name)=``), blockquotes (``% comment``) and block breaks (``+++``).
    
    :param single_line_directive: Parse single line directives
    """
    md.block.ruler.before(
        "blockquote",
        "myst_line_comment",
        line_comment,
        {"alt": ["paragraph", "reference", "blockquote", "list", "footnote_def"]},
    )
    md.block.ruler.before(
        "hr",
        "myst_block_break",
        block_break,
        {"alt": ["paragraph", "reference", "blockquote", "list", "footnote_def"]},
    )
    md.block.ruler.before(
        "hr",
        "myst_target",
        target,
        {"alt": ["paragraph", "reference", "blockquote", "list", "footnote_def"]},
    )
    if single_line_directives:
        md.block.ruler.before(
        "fence",
        "myst_single_line_directive",
        partial(single_line_directive, markers=sld_markers),
        {"alt": []},
    )
    md.add_render_rule("myst_target", render_myst_target)
    md.add_render_rule("myst_line_comment", render_myst_line_comment)


def line_comment(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    if is_code_block(state, startLine):
        return False

    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    if state.src[pos] != "%":
        return False

    if silent:
        return True

    token = state.push("myst_line_comment", "", 0)
    token.attrSet("class", "myst-line-comment")
    token.content = state.src[pos + 1 : maximum].rstrip()
    token.markup = "%"

    # search end of block while appending lines to `token.content`
    for nextLine in itertools.count(startLine + 1):
        if nextLine >= endLine:
            break
        pos = state.bMarks[nextLine] + state.tShift[nextLine]
        maximum = state.eMarks[nextLine]

        if state.src[pos] != "%":
            break
        token.content += "\n" + state.src[pos + 1 : maximum].rstrip()

    state.line = nextLine
    token.map = [startLine, nextLine]

    return True


def block_break(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    if is_code_block(state, startLine):
        return False

    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    marker = state.src[pos]
    pos += 1

    # Check block marker
    if marker != "+":
        return False

    # markers can be mixed with spaces, but there should be at least 3 of them

    cnt = 1
    while pos < maximum:
        ch = state.src[pos]
        if ch != marker and ch not in ("\t", " "):
            break
        if ch == marker:
            cnt += 1
        pos += 1

    if cnt < 3:
        return False

    if silent:
        return True

    state.line = startLine + 1

    token = state.push("myst_block_break", "hr", 0)
    token.attrSet("class", "myst-block")
    token.content = state.src[pos:maximum].strip()
    token.map = [startLine, state.line]
    token.markup = marker * cnt

    return True


def target(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    if is_code_block(state, startLine):
        return False

    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    text = state.src[pos:maximum].strip()
    if not text.startswith("("):
        return False
    if not text.endswith(")="):
        return False
    if not text[1:-2]:
        return False

    if silent:
        return True

    state.line = startLine + 1

    token = state.push("myst_target", "", 0)
    token.attrSet("class", "myst-target")
    token.content = text[1:-2]
    token.map = [startLine, state.line]

    return True


def single_line_directive(state: StateBlock, startLine: int, endLine: int, silent: bool, markers: str = "`~") -> bool:
    if is_code_block(state, startLine):
        return False

    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    text = state.src[pos:maximum].strip()

    for ch in markers:
        if text.startswith(ch*3) and text[3:].startswith("{") and text.endswith(ch*3):
            splt = text[3:-3].split(maxsplit=1)
            name = splt[0]
            content = "" if len(splt) == 1 else splt[1]
            if name.endswith("}") and len(name) > 2:
                break
    else:
        return False
    
    if silent:
        return True

    state.line = startLine + 1

    token = state.push("fence", "code", 0)
    token.info = name
    token.content = content
    token.markup = ch
    token.map = [startLine, state.line]

    return True


def render_myst_target(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    label = tokens[idx].content
    class_name = "myst-target"
    target = f'<a href="#{label}">({label})=</a>'
    return f'<div class="{class_name}">{target}</div>'


def render_myst_line_comment(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    options: OptionsDict,
    env: EnvType,
) -> str:
    # Strip leading whitespace from all lines
    content = "\n".join(line.lstrip() for line in tokens[idx].content.split("\n"))
    return f"<!-- {escapeHtml(content)} -->"
