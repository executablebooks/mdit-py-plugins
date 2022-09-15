from pathlib import Path
from textwrap import dedent

import pytest
from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file

from mdit_py_plugins.fancy_list import fancy_list_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "fancy_list.md")


def test_plugin_parse(data_regression):
    md = MarkdownIt().use(fancy_list_plugin)
    tokens = md.parse(
        dedent(
            """\
    :abc: Content
    :def: Content
    """
        )
    )
    data_regression.check([t.as_dict() for t in tokens])


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(
        fancy_list_plugin, allow_ordinal="(ordinal)" in title
    )
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()
