from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.front_matter import front_matter_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "front_matter.md")


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(front_matter_plugin)
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


def test_token():
    md = MarkdownIt("commonmark").use(front_matter_plugin)
    tokens = md.parse("---\na: 1\n---")
    # print(tokens)
    assert tokens == [
        Token(
            type="front_matter",
            tag="",
            nesting=0,
            attrs=None,
            map=[0, 3],
            level=0,
            children=None,
            content="a: 1",
            markup="---",
            info="",
            meta={},
            block=True,
            hidden=True,
        )
    ]


@pytest.mark.parametrize("closer", ["---", "..."])
def test_token_content_excludes_the_closer(closer):
    """The closing marker must not be left inside the extracted content.

    ``...`` is the YAML document-end marker and is exercised by the fixture file,
    so it has to be consumed like the dashed form rather than kept in the block.
    """
    md = MarkdownIt("commonmark").use(front_matter_plugin)
    tokens = md.parse(f"---\na: 1\n{closer}")
    assert [token.type for token in tokens] == ["front_matter"]
    assert tokens[0].content == "a: 1"


def test_dots_closer_on_the_last_line():
    """A block closed by ``...`` on the final line is still front matter.

    ``test_all`` cannot see this: the front_matter token is hidden, so only the
    rendered output is asserted, and a block that is dropped rather than closed
    renders as visible text instead of disappearing.
    """
    md = MarkdownIt("commonmark").use(front_matter_plugin)
    assert md.render("---\na: 1\n...\n") == md.render("---\na: 1\n---\n") == ""


def test_short_source():
    md = MarkdownIt("commonmark").use(front_matter_plugin)

    # The code should not raise an IndexError.
    assert md.parse("-")
