import json
from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.wordcount import wordcount_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "wordcount.md")


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(wordcount_plugin, store_text="(text)" in title)
    env = {}
    md.render(input, env)
    data = json.dumps(env["wordcount"], indent=2, sort_keys=True)
    try:
        assert data.strip() == expected.strip()
    except AssertionError:
        print(data)
        raise
