"""Tests for the GFM autolink extension plugin."""

from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.gfm_autolink import gfm_autolink_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "gfm_autolink.md")


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_gfm_autolink_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(gfm_autolink_plugin)
    md.options.xhtmlOut = False
    text = md.render(input)
    try:
        assert text.rstrip() == expected.rstrip()
    except AssertionError:
        print(text)
        raise
