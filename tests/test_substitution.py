from pathlib import Path
from textwrap import dedent

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

# from markdown_it.token import Token
from mdit_py_plugins.substitution import substitution_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "substitution.md")


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").enable("table").use(substitution_plugin)
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


def test_tokens(data_regression):
    md = MarkdownIt().use(substitution_plugin)
    tokens = md.parse(
        dedent(
            """\
    {{ block }}

    a {{ inline }} b
    """
        )
    )
    data_regression.check([t.as_dict() for t in tokens])
