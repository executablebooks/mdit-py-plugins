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


@pytest.mark.parametrize("closer", ["---", "...", "...   "])
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


@pytest.mark.parametrize(
    "marker,content", [("+", 'title = "Hello"'), (";", '{"title": "Hello"}')]
)
def test_custom_marker(marker, content):
    md = MarkdownIt("commonmark").use(front_matter_plugin, marker=marker)
    source = f"{marker * 3}\n{content}\n{marker * 3}\n# Head"
    tokens = md.parse(source)

    assert tokens[0].type == "front_matter"
    assert tokens[0].content == content
    assert tokens[0].markup == marker * 3
    assert tokens[0].map == [0, 3]
    assert tokens[0].hidden
    assert tokens[0].block
    assert md.render(source) == "\n<h1>Head</h1>\n"


@pytest.mark.parametrize(
    "opening,closing", [("+++", "+++"), ("++++", "+++++"), ("+++  ", "+++\t ")]
)
def test_custom_marker_empty_metadata(opening, closing):
    md = MarkdownIt().use(front_matter_plugin, marker="+")
    tokens = md.parse(f"{opening}\n{closing}")
    assert len(tokens) == 1
    assert tokens[0].type == "front_matter"
    assert tokens[0].content == ""
    assert tokens[0].map == [0, 2]


@pytest.mark.parametrize(
    "source",
    [
        "",
        "+",
        "++",
        "++\na: 1\n++",
        "+++\na: 1",
        "+++\na: 1\n---",
        "++++\na: 1\n+++",
        "+++\na: 1\n+++ text",
        " +++\na: 1\n+++",
        "\n+++\na: 1\n+++",
        "# Head\n+++\na: 1\n+++",
    ],
)
def test_custom_marker_not_front_matter(source):
    md = MarkdownIt().use(front_matter_plugin, marker="+")
    assert all(token.type != "front_matter" for token in md.parse(source))


def test_custom_marker_keeps_yaml_terminator_as_content():
    md = MarkdownIt().use(front_matter_plugin, marker="+")
    content = 'text = """\n...\n"""'
    source = f"+++\n{content}\n+++\n# Head"
    tokens = md.parse(source)
    assert tokens[0].content == content
    assert tokens[0].map == [0, 5]
    assert md.render(source) == "\n<h1>Head</h1>\n"


def test_marker_configuration_is_per_parser():
    default = MarkdownIt().use(front_matter_plugin)
    custom = MarkdownIt().use(front_matter_plugin, marker="+")
    yaml_source = "---\nx: 1\n---"
    toml_source = "+++\nx = 1\n+++"

    assert default.parse(yaml_source)[0].type == "front_matter"
    assert custom.parse(toml_source)[0].type == "front_matter"
    assert all(token.type != "front_matter" for token in default.parse(toml_source))
    assert all(token.type != "front_matter" for token in custom.parse(yaml_source))


@pytest.mark.parametrize("marker", ["", "++", " ", "\t", "\n", "\x00"])
def test_invalid_marker(marker):
    with pytest.raises(ValueError, match="single non-whitespace character"):
        MarkdownIt().use(front_matter_plugin, marker=marker)
