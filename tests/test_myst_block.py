from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.myst_blocks import myst_block_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "myst_block.md")


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(myst_block_plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


def test_block_token():
    md = MarkdownIt("commonmark").use(myst_block_plugin)
    tokens = md.parse("+++")
    expected_token = Token(
        type="myst_block_break",
        tag="hr",
        nesting=0,
        map=[0, 1],
        level=0,
        children=None,
        content="",
        markup="+++",
        info="",
        meta={},
        block=True,
        hidden=False,
    )
    expected_token.attrSet("class", "myst-block")
    assert tokens == [expected_token]

    tokens = md.parse("\n+ + + abc")
    expected_token = Token(
        type="myst_block_break",
        tag="hr",
        nesting=0,
        map=[1, 2],
        level=0,
        children=None,
        content="abc",
        markup="+++",
        info="",
        meta={},
        block=True,
        hidden=False,
    )
    expected_token.attrSet("class", "myst-block")
    assert tokens == [expected_token]


def test_comment_token():
    md = MarkdownIt("commonmark").use(myst_block_plugin)
    tokens = md.parse("\n\n% abc \n%def")
    expected_token = Token(
        type="myst_line_comment",
        tag="",
        nesting=0,
        map=[2, 4],
        level=0,
        children=None,
        content=" abc\ndef",
        markup="%",
        info="",
        meta={},
        block=True,
        hidden=False,
    )
    expected_token.attrSet("class", "myst-line-comment")
    assert tokens == [expected_token]
