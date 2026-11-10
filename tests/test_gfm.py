"""Tests for the composite GFM plugin."""

from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.gfm import gfm_plugin

# The plugin needs markdown-it-py >= 4.1.0 (it raises RuntimeError below that);
# the guard itself is tested in test_mdit_version_guard.py, on every version.
pytest.importorskip("markdown_it", minversion="4.1.0")

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "gfm.md")


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_gfm_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(
        gfm_plugin, dollarmath="dollar math" in title.lower()
    )
    md.options["xhtmlOut"] = False
    text = md.render(input)
    try:
        assert text.rstrip() == expected.rstrip()
    except AssertionError:
        print(text)
        raise
