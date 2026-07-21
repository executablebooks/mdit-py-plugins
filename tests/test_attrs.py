from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.attrs import attrs_block_plugin, attrs_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures")


@pytest.mark.parametrize(
    "line,title,input,expected", read_fixture_file(FIXTURE_PATH / "attrs.md")
)
def test_attrs(line, title, input, expected):
    md = MarkdownIt("commonmark").use(attrs_plugin, spans=True).use(attrs_block_plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


def test_attrs_allowed(data_regression):
    allowed = ["safe"]
    md = (
        MarkdownIt("commonmark")
        .use(attrs_plugin, allowed=allowed)
        .use(attrs_block_plugin, allowed=allowed)
    )
    tokens = md.parse("""
{danger1=a safe=b}
{danger2=c safe=d}
# header

`inline`{safe=a danger=b}
    """)
    data_regression.check([t.as_dict() for t in tokens])


@pytest.mark.parametrize(
    "src,leaked",
    [
        ('[x]{onclick="alert(1)"}', "onclick"),
        ('[x]{OnClick="alert(1)"}', "onclick"),  # case-insensitive
        ('[x]{style="color:red"}', "style"),
        ('![a](i.png){onerror="alert(1)"}', "onerror"),
    ],
)
def test_event_handler_and_style_stripped_by_default(src, leaked):
    """With no ``allowed`` list, on* and style attributes are removed (XSS)."""
    md = MarkdownIt("commonmark").use(attrs_plugin, spans=True).use(attrs_block_plugin)
    text = md.render(src)
    assert leaked.lower() not in text.lower()


def test_block_event_handler_stripped_by_default():
    md = MarkdownIt("commonmark").use(attrs_plugin).use(attrs_block_plugin)
    text = md.render('{onmouseover="alert(1)"}\nparagraph\n')
    assert "onmouseover" not in text


def test_benign_attrs_preserved_by_default():
    """The insecure-by-default baseline only strips on*/style, not benign attrs."""
    md = MarkdownIt("commonmark").use(attrs_plugin, spans=True)
    text = md.render("[x]{#a .b width=100 data-y=z}")
    assert 'id="a"' in text
    assert 'width="100"' in text
    assert 'data-y="z"' in text


def test_span_respects_allowed_list():
    """Spans now honour an explicit allow-list (previously bypassed entirely)."""
    md = MarkdownIt("commonmark").use(attrs_plugin, spans=True, allowed=["id", "class"])
    text = md.render("[x]{#a .b width=100 onclick=e}")
    assert 'id="a"' in text
    assert "width" not in text
    assert "onclick" not in text
