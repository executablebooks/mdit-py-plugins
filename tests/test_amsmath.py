from pathlib import Path
from textwrap import dedent

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.amsmath import amsmath_plugin

FIXTURE_PATH = Path(__file__).parent


def test_plugin_parse(data_regression):
    md = MarkdownIt().use(amsmath_plugin)
    tokens = md.parse(
        dedent(
            """\
    a
    \\begin{equation}
    b=1
    c=2
    \\end{equation}
    d
    """
        )
    )
    data_regression.check([t.as_dict() for t in tokens])


def test_custom_renderer(data_regression):
    md = MarkdownIt().use(amsmath_plugin, renderer=lambda x: x + "!")
    output = md.render("\\begin{equation}\na\n\\end{equation}")
    assert (
        output.strip()
        == dedent(
            """\
        <div class="math amsmath">
        \\begin{equation}
        a
        \\end{equation}!
        </div>
        """
        ).strip()
    )


@pytest.mark.parametrize(
    "line,title,input,expected",
    read_fixture_file(FIXTURE_PATH.joinpath("fixtures", "amsmath.md")),
)
def test_fixtures(line, title, input, expected):
    md = MarkdownIt("commonmark").use(amsmath_plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()
