from pathlib import Path
import re
from textwrap import dedent

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.tasklists import tasklists_plugin

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "tasklists.md")


def test_plugin_parse(data_regression):
    md = MarkdownIt().use(tasklists_plugin)
    tokens = md.parse(
        dedent(
            """\
    * [ ] Task incomplete
    * [x] Task complete
      * [ ] Indented task incomplete
      * [x] Indented task complete
    """
        )
    )
    data_regression.check([t.as_dict() for t in tokens])


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(tasklists_plugin)
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


@pytest.mark.parametrize(
    "source,label",
    [
        pytest.param(
            "- [ ] <img src=x onerror=alert(1)>\n",
            " &lt;img src=x onerror=alert(1)&gt;",
            id="raw-html",
        ),
        pytest.param("- [x] a & b\n", " a &amp; b", id="ampersand"),
        pytest.param("- [ ] plain task\n", " plain task", id="plain"),
    ],
)
def test_label_after_is_escaped(source, label):
    """The ``label_after`` label must not carry raw HTML from the source (#143).

    The label is built from the item's source text and emitted as an
    ``html_inline`` token, so it used to bypass ``html=False``.
    """
    md = MarkdownIt("commonmark", {"html": False}).use(
        tasklists_plugin, label=True, label_after=True
    )
    text = re.sub(r"task-item-[0-9a-f-]+", "task-item-ID", md.render(source))
    checked = ' checked="checked"' if source.startswith("- [x]") else ""
    assert text == (
        '<ul class="contains-task-list">\n'
        '<li class="task-list-item"><input class="task-list-item-checkbox"'
        f'{checked} disabled="disabled" type="checkbox" id="task-item-ID">'
        f'<label class="task-list-item-label" for="task-item-ID">{label}</label>'
        "</li>\n</ul>\n"
    )
