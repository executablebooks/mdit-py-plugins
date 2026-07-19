from pathlib import Path
from types import SimpleNamespace

from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.section_ref import section_ref_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "section_ref.md")


def test_token():
    md = MarkdownIt().use(section_ref_plugin)
    src = "see §1.2 here"
    tokens = md.parse(src)
    print(tokens)
    assert tokens == [
        Token(
            type="paragraph_open",
            tag="p",
            nesting=1,
            attrs=None,
            map=[0, 1],
            level=0,
            children=None,
            content="",
            markup="",
            info="",
            meta={},
            block=True,
            hidden=False,
        ),
        Token(
            type="inline",
            tag="",
            nesting=0,
            attrs=None,
            map=[0, 1],
            level=1,
            children=[
                Token(
                    type="text",
                    tag="",
                    nesting=0,
                    attrs=None,
                    map=None,
                    level=0,
                    children=None,
                    content="see ",
                    markup="",
                    info="",
                    meta={},
                    block=False,
                    hidden=False,
                ),
                Token(
                    type="section_ref",
                    tag="",
                    nesting=0,
                    attrs=None,
                    map=None,
                    level=0,
                    children=None,
                    content="§1.2",
                    markup="§",
                    info="",
                    meta={"numbers": [1, 2]},
                    block=False,
                    hidden=False,
                ),
                Token(
                    type="text",
                    tag="",
                    nesting=0,
                    attrs=None,
                    map=None,
                    level=0,
                    children=None,
                    content=" here",
                    markup="",
                    info="",
                    meta={},
                    block=False,
                    hidden=False,
                ),
            ],
            content="see §1.2 here",
            markup="",
            info="",
            meta={},
            block=True,
            hidden=False,
        ),
        Token(
            type="paragraph_close",
            tag="p",
            nesting=-1,
            attrs=None,
            map=None,
            level=0,
            children=None,
            content="",
            markup="",
            info="",
            meta={},
            block=True,
            hidden=False,
        ),
    ]


def test_runtime_error():
    """The plugin requires the ``add_terminator_char`` API (markdown-it-py >= 4.1.0)."""
    md = MarkdownIt()
    md.inline = SimpleNamespace()  # type: ignore[assignment]  # lacks add_terminator_char
    with pytest.raises(RuntimeError, match="requires markdown-it-py"):
        section_ref_plugin(md)


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(section_ref_plugin)
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()
