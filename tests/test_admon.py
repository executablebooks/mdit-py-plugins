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


def _best_render_seconds(md: MarkdownIt, source: str, limit: float) -> float:
    """Fastest of three renders, stopping early once one exceeds ``limit``."""
    best = float("inf")
    for _ in range(3):
        start = time.perf_counter()
        md.render(source)
        best = min(best, time.perf_counter() - start)
        if best > limit:
            break
    return best


@pytest.mark.timeout(60)
def test_header_redos():
    """A multi-tag header with a long unquoted space run parses in linear time.

    The title pattern ``[^"]+\\s+"`` backtracked quadratically on this input (#143),
    taking seconds at 100k characters.
    The guard compares two run lengths instead of asserting a time budget,
    so it does not depend on how fast the machine is:
    a run four times longer takes about 4x as long when parsing is linear,
    and about 16x when it is quadratic.
    """
    md = MarkdownIt().use(admon_plugin)

    def source(run: int) -> str:
        return "!!! note a" + " " * run + "b\n    content"

    small = _best_render_seconds(md, source(25_000), float("inf"))
    large = _best_render_seconds(md, source(100_000), 8 * small)
    assert large < 8 * small, (
        f"25k run: {small:.4f}s, 100k run: {large:.4f}s ({large / small:.1f}x); "
        "the admon header parse is super-linear (ReDoS)"
    )
