from pathlib import Path
from textwrap import dedent

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock
from markdown_it.rules_inline import StateInline
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.dollarmath import index as main

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures")


def test_inline_func():
    inline_func = main.math_inline_dollar()

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
    block_func = main.math_block_dollar()
    md = MarkdownIt()
    src = r"$$\na=1\n\nc\nb=2$$ (abc)"
    tokens = []
    state = StateBlock(src, md, {}, tokens)
    block_func(state, 0, 10, False)
    print(tokens[0].as_dict())
    assert tokens[0].as_dict() == {
        "type": "math_block_label",
        "tag": "math",
        "nesting": 0,
        "attrs": None,
        "map": [0, 1],
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
    md = MarkdownIt().use(dollarmath_plugin)
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


def test_custom_renderer(data_regression):
    md = MarkdownIt().use(dollarmath_plugin, renderer=lambda x, y: x)
    assert md.render("$x$").strip() == '<p><span class="math inline">x</span></p>'


@pytest.mark.parametrize(
    "line,title,input,expected",
    read_fixture_file(FIXTURE_PATH.joinpath("dollar_math.md")),
)
def test_dollarmath_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(
        dollarmath_plugin,
        allow_space=False,
        allow_digits=False,
        double_inline=True,
        allow_blank_lines=False,
    )
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options.xhtmlOut = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


# no parentheses inside the label, or it is not parsed as one
_LABEL_XSS = '$$\na=1\n$$ ("><svg onload=alert`1`>)\n'


@pytest.mark.parametrize(
    "label_normalizer,label",
    [
        pytest.param(
            None,
            "&quot;&gt;&lt;svg-onload=alert`1`&gt;",
            id="default-normalizer",
        ),
        pytest.param(
            lambda label: label,
            "&quot;&gt;&lt;svg onload=alert`1`&gt;",
            id="identity-normalizer",
        ),
    ],
)
def test_label_is_html_escaped(label_normalizer, label):
    """The label must not break out of the ``id`` and ``href`` attributes (#143)."""
    md = MarkdownIt("commonmark", {"html": False}).use(
        dollarmath_plugin, label_normalizer=label_normalizer
    )
    # the payload must reach the label renderer, not fall back to a paragraph
    assert [t.type for t in md.parse(_LABEL_XSS)] == ["math_block_label"]
    assert md.render(_LABEL_XSS) == (
        f'<div id="{label}" class="math block">\n'
        f'<a href="#{label}" class="mathlabel" title="Permalink to this equation">'
        "¶</a>\na=1\n</div>\n"
    )
