from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.abbr import abbr_plugin

FIXTURE_PATH = Path(__file__).parent


@pytest.mark.parametrize(
    "line,title,input,expected",
    read_fixture_file(FIXTURE_PATH.joinpath("fixtures", "abbr.md")),
)
def test_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(abbr_plugin)
    text = md.render(input)
    assert text.rstrip() == expected.rstrip()
