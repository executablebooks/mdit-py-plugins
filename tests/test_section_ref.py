from pathlib import Path
import time

from markdown_it import MarkdownIt
from markdown_it.token import Token
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.section_ref import section_ref_plugin

# The plugin needs markdown-it-py >= 4.1.0 (it raises RuntimeError below that);
# the guard itself is tested in test_mdit_version_guard.py, on every version.
pytest.importorskip("markdown_it", minversion="4.1.0")

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures", "section_ref.md")


def test_token():
    md = MarkdownIt().use(section_ref_plugin)
    src = "see §1.2 here"
    tokens = md.parse(src)
    print(tokens)
    assert tokens == [
        Token(
            type="paragraph_open",
            tag="p",
            nesting=1,
            attrs=None,
            map=[0, 1],
            level=0,
            children=None,
            content="",
            markup="",
            info="",
            meta={},
            block=True,
            hidden=False,
        ),
        Token(
            type="inline",
            tag="",
            nesting=0,
            attrs=None,
            map=[0, 1],
            level=1,
            children=[
                Token(
                    type="text",
                    tag="",
                    nesting=0,
                    attrs=None,
                    map=None,
                    level=0,
                    children=None,
                    content="see ",
                    markup="",
                    info="",
                    meta={},
                    block=False,
                    hidden=False,
                ),
                Token(
                    type="section_ref",
                    tag="",
                    nesting=0,
                    attrs=None,
                    map=None,
                    level=0,
                    children=None,
                    content="§1.2",
                    markup="§",
                    info="",
                    meta={"numbers": [1, 2]},
                    block=False,
                    hidden=False,
                ),
                Token(
                    type="text",
                    tag="",
                    nesting=0,
                    attrs=None,
                    map=None,
                    level=0,
                    children=None,
                    content=" here",
                    markup="",
                    info="",
                    meta={},
                    block=False,
                    hidden=False,
                ),
            ],
            content="see §1.2 here",
            markup="",
            info="",
            meta={},
            block=True,
            hidden=False,
        ),
        Token(
            type="paragraph_close",
            tag="p",
            nesting=-1,
            attrs=None,
            map=None,
            level=0,
            children=None,
            content="",
            markup="",
            info="",
            meta={},
            block=True,
            hidden=False,
        ),
    ]


def test_token_shape_is_public_api():
    """Every field of the ``section_ref`` token, which is public API from 0.7.0.

    Downstream renderers (MyST-Parser) and ports of the grammar (ubCode) read
    these fields directly, so changing any of them is a breaking change.
    """
    md = MarkdownIt().use(section_ref_plugin)
    children = md.parseInline("§01.02")[0].children
    assert children is not None
    assert len(children) == 1
    token = children[0]
    assert token.type == "section_ref"
    assert token.nesting == 0
    assert token.children is None
    assert token.tag == ""
    assert token.attrs == {}
    assert token.markup == "§"
    assert token.content == "§01.02"
    assert token.meta == {"numbers": [1, 2]}


@pytest.mark.parametrize("line,title,input,expected", read_fixture_file(FIXTURE_PATH))
def test_all(line, title, input, expected):
    md = MarkdownIt("commonmark").use(section_ref_plugin)
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


def test_huge_digit_run_renders_as_text():
    """``§`` + 5000 digits must not raise (``int()`` refuses > 4300 digits).

    The over-long level makes the rule decline, so the text renders literally.
    """
    md = MarkdownIt().use(section_ref_plugin)
    digits = "1" * 5000
    assert md.render(f"see §{digits}") == f"<p>see §{digits}</p>\n"
    tokens = md.parseInline(f"see §{digits}")[0].children
    assert tokens is not None
    assert [t.type for t in tokens] == ["text"]


@pytest.mark.parametrize(
    "src,numbers",
    [
        ("§999999999", [999999999]),
        ("§1.999999999.2", [1, 999999999, 2]),
        ("§000000001", [1]),
    ],
)
def test_numbers_at_bound(src, numbers):
    """A level of exactly nine digits is still a reference, with its int value."""
    md = MarkdownIt().use(section_ref_plugin)
    tokens = md.parseInline(src)[0].children
    assert tokens is not None
    assert [t.type for t in tokens] == ["section_ref"]
    assert tokens[0].content == src
    assert tokens[0].meta == {"numbers": numbers}


@pytest.mark.parametrize(
    "src",
    ["§1234567890", "§1.1234567890", "§1234567890.1", "§1.2.1234567890.3"],
)
def test_level_past_bound_declines(src):
    """Any level past nine digits makes the whole text literal (no prefix match)."""
    md = MarkdownIt().use(section_ref_plugin)
    tokens = md.parseInline(src)[0].children
    assert tokens is not None
    assert [t.type for t in tokens] == ["text"]
    assert tokens[0].content == src


@pytest.mark.parametrize(
    "src",
    [
        "§" + "1" * 200_000,
        "§" + "1." * 100_000 + "1" * 10,
        ("§" + "1" * 5000 + " ") * 40,
    ],
    ids=["one-run", "dotted-run", "many-runs"],
)
def test_long_digit_runs_stay_fast(src):
    """Long digit runs are scanned in linear time, with no backtracking blow-up.

    A scan that does Python-level work per character, quadratic in the input
    (up to 200k characters), or a backtracking regex would take far longer than
    the budget. The budget leaves room for slow CI runners and coverage, so a
    quadratic scan built from string slices or copies can still pass it.
    """
    md = MarkdownIt().use(section_ref_plugin)
    start = time.perf_counter()
    md.render(src)
    elapsed = time.perf_counter() - start
    assert elapsed < 3.0, f"render took {elapsed:.3f}s for {len(src)} characters"
