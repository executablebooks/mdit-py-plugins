from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.anchors.index import slugify
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


@pytest.mark.parametrize(
    "source, expected_ids",
    [
        pytest.param(
            "{#foo}\n### Bar\n\n# Foo",
            ["foo", "foo-1"],
            id="out-of-level-id-reserved",
        ),
        pytest.param(
            "{#a}\n# X\n\n{#a}\n# Y",
            ["a", "a"],
            id="duplicate-explicit-ids-kept",
        ),
        pytest.param(
            '{id=""}\n# Title',
            ["title"],
            id="empty-id-is-generated",
        ),
        pytest.param(
            '{id=""}\n# Title\n\n# Title',
            ["title", "title-1"],
            id="empty-id-not-reserved",
        ),
    ],
)
def test_explicit_heading_id_edge_cases(source: str, expected_ids: list[str]) -> None:
    """Pin the edge cases of explicit heading IDs.

    An explicit ID outside the selected levels is still reserved,
    duplicate explicit IDs are kept as written (no error is raised),
    and an empty ID (invalid in HTML) is treated as absent.
    """
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
    assert 'id=""' not in rendered
    assert 'href="#"' not in rendered


def test_explicit_heading_id_plugin_order() -> None:
    """The explicit ID is kept whichever plugin is loaded first."""
    md = MarkdownIt("commonmark").use(anchors_plugin).use(attrs_block_plugin)
    assert md.render("{#custom}\n# Heading") == '<h1 id="custom">Heading</h1>\n'


@pytest.mark.parametrize(
    "source, expected_id",
    [
        pytest.param("# Foo", "foo", id="plain"),
        pytest.param("# Foo ![img](x.png)", "foo-", id="trailing-image"),
        pytest.param("# ![img](x.png) Foo", "-foo", id="leading-image"),
        pytest.param("# Foo <br>", "foo-", id="trailing-html"),
        pytest.param("# &#32;Foo", "-foo", id="leading-entity-space"),
    ],
)
def test_slug_keeps_edge_whitespace(source: str, expected_id: str) -> None:
    """Whitespace at the edges of the title text is not stripped before slugifying.

    The title text is joined from the ``text`` and ``code_inline`` children only,
    so a space next to an image, raw HTML or an entity survives as a hyphen.
    This matches MyST-Parser's ``github_slugify`` (and so its heading anchors).
    """
    md = MarkdownIt("commonmark").use(anchors_plugin)
    tokens = md.parse(source)
    assert [
        token.attrGet("id") for token in tokens if token.type == "heading_open"
    ] == [expected_id]


@pytest.mark.parametrize(
    "title, expected",
    [(" a b ", "-a-b-"), ("a b  c", "a-b--c"), ("Foo", "foo")],
)
def test_slugify(title: str, expected: str) -> None:
    """The default slug function lowercases, hyphenates spaces, and does not strip."""
    assert slugify(title) == expected
