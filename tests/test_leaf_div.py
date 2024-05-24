from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.leaf_directive import leaf_directive_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures")


@pytest.mark.parametrize(
    "line,title,input,expected", read_fixture_file(FIXTURE_PATH / "leaf_directive.md")
)
def test_fixture(line, title, input, expected):
    md = MarkdownIt("commonmark").use(leaf_directive_plugin)
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


def test_no_content_parse(data_regression):
    md = MarkdownIt().use(leaf_directive_plugin, parse_content=False)
    tokens = md.parse("::name content\nmultiline")
    data_regression.check([t.as_dict() for t in tokens])
