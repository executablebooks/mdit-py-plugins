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
