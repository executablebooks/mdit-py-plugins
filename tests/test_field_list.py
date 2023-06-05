from pathlib import Path
from textwrap import dedent

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.field_list import fieldlist_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "field_list.md")


def test_plugin_parse(data_regression):
    md = MarkdownIt().use(fieldlist_plugin)
    tokens = md.parse(
        dedent(
            """\
    :abc: Content
    :def: Content
    """
        )
    )
    data_regression.check([t.as_dict() for t in tokens])


fixtures = read_fixture_file(FIXTURE_PATH)


@pytest.mark.parametrize(
    "line,title,input,expected",
    fixtures,
    ids=[f"{f[0]}-{f[1].replace(' ', '_')}" for f in fixtures],
)
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(fieldlist_plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()
