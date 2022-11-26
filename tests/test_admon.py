from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.admon import admon_plugin

FIXTURE_PATH = Path(__file__).parent


@pytest.mark.parametrize(
    "line,title,input,expected",
    read_fixture_file(FIXTURE_PATH.joinpath("fixtures", "admon.md")),
)
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(admon_plugin)
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()
