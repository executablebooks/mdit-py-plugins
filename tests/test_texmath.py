from pathlib import Path
from textwrap import dedent

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.rules_inline import StateInline
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.texmath import index as main
from mdit_py_plugins.texmath import texmath_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures")


def test_inline_func():
    inline_func = main.make_inline_func(main.rules["dollars"]["inline"][0])

    md = MarkdownIt()
    src = r"$a=1$ $b=2$"
    tokens = []
    state = StateInline(src, md, {}, tokens)
    inline_func(state, False)
    assert tokens[0].as_dict() == {
        "type": "math_inline",
        "tag": "math",
        "nesting": 0,
        "attrs": None,
        "map": None,
        "level": 0,
        "children": None,
        "content": "a=1",
        "markup": "$",
        "info": "",
        "meta": {},
        "block": False,
        "hidden": False,
    }
    assert state.pos == 5


def test_block_func():
    block_func = main.make_block_func(main.rules["dollars"]["block"][0])
    md = MarkdownIt()
    src = r"$$\na=1\n\nc\nb=2$$ (abc)"
    tokens = []
    state = StateBlock(src, md, {}, tokens)
    block_func(state, 0, 10, False)
    assert tokens[0].as_dict() == {
        "type": "math_block_eqno",
        "tag": "math",
        "nesting": 0,
        "attrs": None,
        "map": None,
        "level": 0,
        "children": None,
        "content": "\\na=1\\n\\nc\\nb=2",
        "markup": "$$",
        "info": "abc",
        "meta": {},
        "block": True,
        "hidden": False,
    }


def test_plugin_parse(data_regression):
    md = MarkdownIt().use(texmath_plugin)
    tokens = md.parse(
        dedent(
            """\
    $$
    a=1
    b=2
    $$ (abc)

    - ab $c=1$ d
    """
        )
    )
    data_regression.check([t.as_dict() for t in tokens])


@pytest.mark.parametrize(
    "delimiters,opening,closing",
    [
        ("brackets", "\\[", "\\]"),
        ("dollars", "$$", "$$"),
        ("kramdown", "$$", "$$"),
        ("gitlab", "```math", "```"),
        ("julia", "```math", "```"),
    ],
)
def test_block_closed_outside_blockquote(delimiters, opening, closing):
    """A math block opened inside a blockquote cannot close after it."""
    md = MarkdownIt("commonmark").use(texmath_plugin, delimiters=delimiters)
    tokens = md.parse(f"> {opening} a=1\n\n{closing}\n")
    assert not [t for t in tokens if t.type.startswith("math_block")]


@pytest.mark.parametrize(
    "line,title,input,expected",
    read_fixture_file(FIXTURE_PATH.joinpath("texmath_dollar.md")),
)
def test_dollar_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(texmath_plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


@pytest.mark.parametrize(
    "line,title,input,expected",
    read_fixture_file(FIXTURE_PATH.joinpath("texmath_bracket.md")),
)
def test_bracket_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(texmath_plugin, delimiters="brackets")
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


@pytest.mark.parametrize("delimiters", ["dollars", "brackets", "gitlab", "julia"])
def test_math_content_is_html_escaped(delimiters):
    """Math content must be HTML-escaped so it cannot inject markup (XSS)."""
    md = MarkdownIt("commonmark").use(texmath_plugin, delimiters=delimiters)
    open_delim = {"dollars": "$", "brackets": r"\(", "gitlab": "$`", "julia": "``"}[
        delimiters
    ]
    close_delim = {"dollars": "$", "brackets": r"\)", "gitlab": "`$", "julia": "``"}[
        delimiters
    ]
    payload = "<img src=x onerror=alert(1)>"
    text = md.render(f"a {open_delim}{payload}{close_delim} b")
    assert "<img" not in text
    assert "&lt;img src=x onerror=alert(1)&gt;" in text


@pytest.mark.parametrize("delimiters", ["gitlab", "julia"])
def test_fenced_math_block(delimiters):
    md = MarkdownIt("commonmark").use(texmath_plugin, delimiters=delimiters)
    text = md.render("```math\n\\alpha = 1\n```\n")
    assert "<eqn>\\alpha = 1</eqn>" in text


@pytest.mark.parametrize("delimiters", ["gitlab", "julia"])
@pytest.mark.parametrize(
    "source,expected",
    [
        ("```math\n  a = 1\n  b = 2\n```\n", ("math_block", "  a = 1\n  b = 2")),
        ("```math\n  a = 1\n``` (1)\n", ("math_block_eqno", "  a = 1", "1")),
    ],
    ids=["math_block", "math_block_eqno"],
)
def test_fenced_math_block_keeps_indent(delimiters, source, expected):
    """The ReDoS fix must not change output: the first line keeps its indentation.

    One whitespace character (the newline after the opening fence) separates
    the fence from the body; a pattern that skips all leading whitespace
    would give the content ``a = 1`` instead.
    The tokens are checked rather than the HTML,
    because every math block renders with the same template.
    """
    md = MarkdownIt("commonmark").use(texmath_plugin, delimiters=delimiters)
    [token] = md.parse(source)
    assert (token.type, token.content, token.info)[: len(expected)] == expected


@pytest.mark.parametrize("delimiters", ["gitlab", "julia"])
@pytest.mark.parametrize(
    "source,expected",
    [
        ("```math\n  \n```\n\nafter\n", ("math_block", " ")),
        ("```math\n  \n``` (1)\n\nafter\n", ("math_block_eqno", " ", "1")),
    ],
    ids=["math_block", "math_block_eqno"],
)
def test_fenced_math_block_whitespace_only(delimiters, source, expected):
    """A body that is only whitespace is still a math block, as it was before #143.

    As a code fence instead, the eqno form would run to the end of the document,
    because ``` ``` (1) ``` cannot close a code fence,
    so the paragraph after it would become code.
    """
    md = MarkdownIt("commonmark").use(texmath_plugin, delimiters=delimiters)
    tokens = md.parse(source)
    assert [t.type for t in tokens] == [
        expected[0],
        "paragraph_open",
        "inline",
        "paragraph_close",
    ]
    assert (tokens[0].type, tokens[0].content, tokens[0].info)[: len(expected)] == (
        expected
    )


@pytest.mark.parametrize("delimiters", ["gitlab", "julia"])
@pytest.mark.timeout(2)
def test_fenced_math_block_redos(delimiters):
    """An unclosed ``` ```math ``` fence must not trigger catastrophic backtracking."""
    md = MarkdownIt("commonmark").use(texmath_plugin, delimiters=delimiters)
    md.render("```math\n" + " " * 20000)
