import gc
from pathlib import Path
from textwrap import dedent
import time

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
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


@pytest.mark.parametrize("text_idx", (0, 1, 2))
def test_plugin_parse(data_regression, text_idx):
    texts = [
        "!!! note\n    content 1",
        "??? note\n    content 2",
        "???+ note\n    content 3",
    ]
    md = MarkdownIt().use(admon_plugin)
    tokens = md.parse(dedent(texts[text_idx]))
    data_regression.check([t.as_dict() for t in tokens])


def _render_seconds(md: MarkdownIt, source: str) -> float:
    """Time one render with the garbage collector paused."""
    gc_was_enabled = gc.isenabled()
    gc.disable()
    try:
        start = time.perf_counter()
        md.render(source)
        return time.perf_counter() - start
    finally:
        if gc_was_enabled:
            gc.enable()


@pytest.mark.timeout(60)
@pytest.mark.parametrize(
    ("header", "filler", "small_run"),
    [
        # tokens + space run: ``[^"]+\s+"`` tried every split of the run
        pytest.param("note a{run}b", " ", 25_000, id="space-run"),
        # quote run: ``"(?P<title>.*)"\S*$`` tried every quote as the closing one
        pytest.param('note "{run} y', '"', 10_000, id="quote-run"),
    ],
)
def test_header_redos(header, filler, small_run):
    """A multi-tag header with a long run of spaces or quotes parses in linear time.

    The title pattern backtracked quadratically on these inputs (#143),
    taking seconds at tens of thousands of characters.
    The guard compares two run lengths instead of asserting a time budget,
    so it does not depend on how fast the machine is:
    a run four times longer takes about 4x as long when parsing is linear,
    and about 16x when it is quadratic.
    The two lengths are timed in alternation and the fastest of each kept,
    stopping once the ratio holds,
    so a single slow sample (a busy machine) does not fail the test,
    while a quadratic parse is slow on every sample.
    Retries also stop once the renders have taken 15 seconds in all,
    which a linear parse (milliseconds per round) never reaches,
    so a regression fails on the assertion rather than the timeout.
    The quote run is shorter, because each quote costs a quadratic parse more.
    """
    md = MarkdownIt().use(admon_plugin)

    def source(run: int) -> str:
        return "!!! " + header.format(run=filler * run) + "\n    content"

    small_source, large_source = source(small_run), source(4 * small_run)
    small = large = float("inf")
    spent = 0.0
    for _ in range(20):
        small_sample = _render_seconds(md, small_source)
        large_sample = _render_seconds(md, large_source)
        small, large = min(small, small_sample), min(large, large_sample)
        spent += small_sample + large_sample
        if large < 8 * small or spent > 15:
            break
    assert large < 8 * small, (
        f"{small_run} run: {small:.4f}s, {4 * small_run} run: {large:.4f}s "
        f"({large / small:.1f}x); the admon header parse is super-linear (ReDoS)"
    )
