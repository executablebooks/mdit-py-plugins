from pathlib import Path
from textwrap import dedent

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.colon_fence import colon_fence_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "colon_fence.md")


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(colon_fence_plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    try:
        assert text.rstrip() == expected.rstrip()
    except AssertionError:
        print(text)
        raise


def test_plugin_parse(data_regression):
    md = MarkdownIt().use(colon_fence_plugin)
    tokens = md.parse(
        dedent(
            """\
    ::: name
    *content*
    :::
    """
        )
    )
    data_regression.check([t.as_dict() for t in tokens])


@pytest.mark.parametrize(
    "source,expected",
    [
        pytest.param(
            ':::a"onmouseover="alert(1)\nx\n:::\n',
            '<pre><code class="block-a&quot;onmouseover=&quot;alert(1)" >x\n'
            "</code></pre>\n",
            id="raw-quote",
        ),
        pytest.param(
            ":::a&quot;&gt;&lt;xss&gt;\nx\n:::\n",
            '<pre><code class="block-a&quot;&gt;&lt;xss&gt;" >x\n</code></pre>\n',
            id="entity-encoded",
        ),
    ],
)
def test_block_name_is_escaped(source, expected):
    """The block name must not break out of the ``class`` attribute (#143).

    With ``html=False`` the output must not carry markup from the source,
    but the name used to be interpolated into the attribute unescaped
    (and the entity-encoded form was unescaped first, then interpolated).
    """
    md = MarkdownIt("commonmark", {"html": False}).use(colon_fence_plugin)
    assert md.render(source) == expected
