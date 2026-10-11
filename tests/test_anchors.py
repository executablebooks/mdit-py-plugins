from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.attrs import attrs_block_plugin

FIXTURE_PATH = Path(__file__).parent


@pytest.mark.parametrize(
    "line,title,input,expected",
    read_fixture_file(FIXTURE_PATH.joinpath("fixtures", "anchors.md")),
)
def test_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(
        anchors_plugin,
        permalink="(permalink" in title,
        permalinkBefore="before)" in title,
    )
    text = md.render(input)
    assert text.rstrip() == expected.rstrip()


@pytest.mark.parametrize(
    "source, expected_ids",
    [
        ("{#custom}\n# Heading", ["custom"]),
        ("{#custom}\n# Heading\n\n# Custom", ["custom", "custom-1"]),
        ("# Custom\n\n{#custom}\n# Heading", ["custom-1", "custom"]),
    ],
)
def test_preserve_explicit_heading_ids(source: str, expected_ids: list[str]) -> None:
    """Preserve explicit anchors and avoid collisions with generated anchors."""
    md = (
        MarkdownIt("commonmark")
        .use(attrs_block_plugin)
        .use(anchors_plugin, permalink=True)
    )
    tokens = md.parse(source)
    assert [
        token.attrGet("id") for token in tokens if token.type == "heading_open"
    ] == expected_ids
    rendered = md.renderer.render(tokens, md.options, {})
    for heading_id in expected_ids:
        assert f'href="#{heading_id}"' in rendered


def test_explicit_heading_id_does_not_call_slug_function() -> None:
    """An explicit heading ID does not need to be generated from its title."""

    def slug_func(title: str) -> str:
        raise AssertionError("Explicit IDs should not be slugified")

    md = (
        MarkdownIt("commonmark")
        .use(attrs_block_plugin)
        .use(anchors_plugin, slug_func=slug_func)
    )
    assert md.render("{#custom}\n# Heading") == '<h1 id="custom">Heading</h1>\n'
