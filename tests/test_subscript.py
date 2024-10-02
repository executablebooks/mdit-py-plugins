"""Tests for subscript plugin."""

from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.subscript import sub_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "subscript.md")
STRIKETHROUGH_FIXTURE_PATH = Path(__file__).parent.joinpath(
    "fixtures", "subscript_strikethrough.md"
)


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_all(line, title, input, expected):
    """Tests for subscript plugin."""
    md = MarkdownIt("commonmark").use(sub_plugin)
    text = md.render(input)
    try:
        assert text.rstrip() == expected.rstrip()
    except AssertionError:
        print(text)
        raise


@pytest.mark.parametrize(
    "line,title,input,expected", read_fixture_file(STRIKETHROUGH_FIXTURE_PATH)
)
def test_all_strikethrough(line, title, input, expected):
    """Tests for subscript plugin with strikethrough enabled."""
    md = MarkdownIt("commonmark").enable("strikethrough").use(sub_plugin)
    text = md.render(input)
    try:
        assert text.rstrip() == expected.rstrip()
    except AssertionError:
        print(text)
        raise
