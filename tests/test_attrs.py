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
        ('![a](i.png){onerror="alert(1)"}', "onerror"),
    ],
)
def test_event_handler_stripped_by_default(src, leaked):
    """With no ``allowed`` list, on* attributes are removed (XSS)."""
    md = MarkdownIt("commonmark").use(attrs_plugin, spans=True).use(attrs_block_plugin)
    text = md.render(src)
    assert leaked.lower() not in text.lower()


def test_block_event_handler_stripped_by_default():
    md = MarkdownIt("commonmark").use(attrs_plugin).use(attrs_block_plugin)
    text = md.render('{onmouseover="alert(1)"}\nparagraph\n')
    assert "onmouseover" not in text


def test_event_handler_moved_to_meta():
    """A removed on* attribute is kept in ``token.meta["insecure_attrs"]``."""
    md = MarkdownIt("commonmark").use(attrs_block_plugin)
    tokens = md.parse("{#a onclick=x}\nparagraph\n")
    assert tokens[0].type == "paragraph_open"
    assert tokens[0].attrs == {"id": "a"}
    assert tokens[0].meta == {"insecure_attrs": {"onclick": "x"}}


@pytest.mark.parametrize(
    "src,token_type,expected",
    [
        pytest.param(
            "{style=lower-alpha}\n1. a\n",
            "ordered_list_open",
            "lower-alpha",
            id="block-list",
        ),
        pytest.param('[x]{style="color:red"}', "span_open", "color:red", id="span"),
        pytest.param(
            '![a](i.png){style="width:1em"}', "image", "width:1em", id="image"
        ),
    ],
)
def test_style_kept_by_default(src, token_type, expected):
    """With no ``allowed`` list, ``style`` is kept (it does not run script).

    MyST-Parser reads ``{style=lower-alpha}`` on an ordered list
    to choose its numbering, so dropping it would break documents.
    """
    md = MarkdownIt("commonmark").use(attrs_plugin, spans=True).use(attrs_block_plugin)
    tokens = md.parse(src)
    found = [t for t in tokens if t.type == token_type]
    found += [c for t in tokens for c in (t.children or []) if c.type == token_type]
    assert len(found) == 1
    assert found[0].attrs.get("style") == expected
    assert "insecure_attrs" not in found[0].meta
    assert f'style="{expected}"' in md.render(src)


def test_benign_attrs_preserved_by_default():
    """The insecure-by-default baseline only strips on*, not benign attrs."""
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


@pytest.mark.parametrize(
    "src,expected,removed",
    [
        pytest.param(
            '[a](https://x){href="javascript:alert(1)"}',
            '<p><a href="https://x">a</a></p>\n',
            {"href": "javascript:alert(1)"},
            id="link-href",
        ),
        pytest.param(
            '[a](https://x){HREF="JavaScript:alert(1)"}',
            '<p><a href="https://x">a</a></p>\n',
            {"HREF": "JavaScript:alert(1)"},
            id="link-href-case",
        ),
        pytest.param(
            '[a](https://x){href="java\tscript:alert(1)"}',
            '<p><a href="https://x">a</a></p>\n',
            {"href": "java\tscript:alert(1)"},
            id="link-href-tab",
        ),
        pytest.param(
            '[a](https://x){href="\x01 javascript:alert(1)"}',
            '<p><a href="https://x">a</a></p>\n',
            {"href": "\x01 javascript:alert(1)"},
            id="link-href-leading-control",
        ),
        pytest.param(
            '![i](x.png){src="javascript:alert(1)"}',
            '<p><img src="x.png" alt="i" /></p>\n',
            {"src": "javascript:alert(1)"},
            id="image-src",
        ),
        pytest.param(
            '[x]{href="vbscript:x"}',
            "<p><span>x</span></p>\n",
            {"href": "vbscript:x"},
            id="span-href",
        ),
        pytest.param(
            '{formaction="javascript:x"}\npara\n',
            "<p>para</p>\n",
            {"formaction": "javascript:x"},
            id="block-formaction",
        ),
        pytest.param(
            '{action="data:text/html,x"}\npara\n',
            "<p>para</p>\n",
            {"action": "data:text/html,x"},
            id="block-action",
        ),
        pytest.param(
            '{xlink:href="javascript:x"}\npara\n',
            "<p>para</p>\n",
            {"xlink:href": "javascript:x"},
            id="block-xlink-href",
        ),
    ],
)
def test_url_attrs_validated(src, expected, removed):
    """URL-valued attributes go through ``md.validateLink``, like link destinations.

    Otherwise ``{href="javascript:..."}`` would bypass the check markdown-it
    applies to ``[a](javascript:...)``, even with ``html=False``.
    """
    md = (
        MarkdownIt("commonmark", {"html": False})
        .use(attrs_plugin, spans=True)
        .use(attrs_block_plugin)
    )
    assert md.render(src) == expected
    tokens = md.parse(src)
    metas = [t.meta for t in tokens] + [
        c.meta for t in tokens for c in (t.children or [])
    ]
    assert {"insecure_attrs": removed} in metas


@pytest.mark.parametrize(
    "src,expected",
    [
        pytest.param(
            '[a](https://x){href="https://ok"}',
            '<p><a href="https://ok">a</a></p>\n',
            id="link-https",
        ),
        pytest.param(
            '[a](https://x){href="#frag"}',
            '<p><a href="#frag">a</a></p>\n',
            id="link-fragment",
        ),
        pytest.param(
            '![i](x.png){src="data:image/png;base64,AAA"}',
            '<p><img src="data:image/png;base64,AAA" alt="i" /></p>\n',
            id="image-data-png",
        ),
        pytest.param(
            '{href="https://ok"}\npara\n',
            '<p href="https://ok">para</p>\n',
            id="block-https",
        ),
    ],
)
def test_url_attrs_valid_kept(src, expected):
    """URLs that ``md.validateLink`` accepts are kept as written."""
    md = (
        MarkdownIt("commonmark", {"html": False})
        .use(attrs_plugin, spans=True)
        .use(attrs_block_plugin)
    )
    assert md.render(src) == expected


def test_url_attrs_validated_when_allowed():
    """An explicit ``allowed`` list does not skip the URL check."""
    md = MarkdownIt("commonmark", {"html": False}).use(attrs_plugin, allowed=["href"])
    src = '[a](https://x){href="javascript:alert(1)"}'
    assert md.render(src) == '<p><a href="https://x">a</a></p>\n'
    link_open = md.parse(src)[1].children[0]
    assert link_open.meta == {"insecure_attrs": {"href": "javascript:alert(1)"}}


def test_url_attrs_use_custom_validate_link():
    """A ``validateLink`` override on the instance is honoured."""
    md = MarkdownIt("commonmark", {"html": False}).use(attrs_block_plugin)
    md.validateLink = lambda url: not url.startswith("https://blocked")  # type: ignore[method-assign]
    assert md.render('{href="https://blocked/x"}\npara\n') == "<p>para</p>\n"
    assert (
        md.render('{href="https://fine/x"}\npara\n')
        == '<p href="https://fine/x">para</p>\n'
    )
