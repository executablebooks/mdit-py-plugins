"""Behavioral ReDoS guard: render adversarial markdown through each plugin.

New plugins add regexes over time. Rather than trust review to catch catastrophic
backtracking, this drives each plugin end-to-end (``MarkdownIt().use(plugin)`` then
``md.render(payload)``) against adversarial input and asserts it stays fast.

Two properties make this faithful to the real attack surface without introspecting
any pattern:

- The payload embeds a long *homogeneous run* of a single character class, which is
  what pushes overlapping or nested quantifiers (e.g. ``\\s+ [^x]+ \\s+``) into
  super-linear backtracking. We fuzz every run character, so we never need to know
  which regex is vulnerable or how it is structured.
- Rendering exercises the *whole* rule chain (the parser re-invoking a block rule
  across offsets), so it also catches the O(n^2) amplification an isolated-regex
  check would miss, and never false-positives on a pattern adversarial input can't
  actually reach.

The only per-plugin cost is one hand-written activation payload: the plugin's public
markdown syntax with a ``{run}`` placeholder for the homogeneous run.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import time

from markdown_it import MarkdownIt
import pytest

from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.amsmath import amsmath_plugin
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.colon_fence import colon_fence_plugin
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.field_list import fieldlist_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
from mdit_py_plugins.myst_role import myst_role_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.texmath import texmath_plugin

# Homogeneous runs of one character class are what drive overlapping/nested
# quantifiers into catastrophic backtracking; fuzz every plugin with each
_FILLERS = [" ", "\t", "$", "`", "\\", '"', "-"]
_RUN = 15_000
_BUDGET_SECONDS = 1.0  # Safe threshold relaxed for CI


@dataclass(frozen=True)
class Case:
    id: str
    configure: Callable[[MarkdownIt], None]
    payload: Callable[[str], str]


_CASES = [
    Case(
        # An interior run with no closing quote: ``[^"]+\s+"`` backtracks the run
        # exhaustively looking for a ``"`` that never comes. A trailing run would be
        # stripped off before the regex sees it, so the run must sit between tokens.
        "admon-header",
        lambda md: md.use(admon_plugin),
        lambda run: f"!!! note a{run}b\n    content",
    ),
    Case(
        "amsmath-open",
        lambda md: md.use(amsmath_plugin),
        lambda run: f"\\begin{{{run}",
    ),
    Case(
        "amsmath-unclosed",
        lambda md: md.use(amsmath_plugin),
        lambda run: f"\\begin{{equation}}\n{run}",
    ),
    Case(
        "anchors-heading",
        lambda md: md.use(anchors_plugin),
        lambda run: f"# {run}",
    ),
    Case(
        "colon-fence",
        lambda md: md.use(colon_fence_plugin),
        lambda run: f"::: {run}\ncontent\n:::",
    ),
    Case(
        "deflist",
        lambda md: md.use(deflist_plugin),
        lambda run: f"term\n:{run}",
    ),
    Case(
        "dollarmath-inline",
        lambda md: md.use(dollarmath_plugin),
        lambda run: f"${run}$",
    ),
    Case(
        "dollarmath-block",
        lambda md: md.use(dollarmath_plugin, allow_labels=True),
        lambda run: f"$$\n{run}",
    ),
    Case(
        "dollarmath-label",
        lambda md: md.use(dollarmath_plugin, allow_labels=True),
        lambda run: f"$$a$$ ({run})",
    ),
    Case(
        "fieldlist",
        lambda md: md.use(fieldlist_plugin),
        lambda run: f":name:{run}",
    ),
    Case(
        "footnote-ref",
        lambda md: md.use(footnote_plugin),
        lambda run: f"[^{run}]: body",
    ),
    Case(
        "myst-block-target",
        lambda md: md.use(myst_block_plugin),
        lambda run: f"({run})=",
    ),
    Case(
        "myst-role",
        lambda md: md.use(myst_role_plugin),
        lambda run: f"{{role}}`{run}`",
    ),
    Case(
        "tasklist",
        lambda md: md.use(tasklists_plugin),
        lambda run: f"- [ ]{run}x",
    ),
    Case(
        "texmath-fence",
        lambda md: md.use(texmath_plugin, delimiters="gitlab"),
        lambda run: f"```math\n{run}",
    ),
    Case(
        "texmath-fence-eqno",
        lambda md: md.use(texmath_plugin, delimiters="gitlab"),
        lambda run: f"```math\n{run}``` (1)",
    ),
    Case(
        "texmath-dollar",
        lambda md: md.use(texmath_plugin, delimiters="dollars"),
        lambda run: f"${run}$",
    ),
]


@pytest.mark.timeout(10)
@pytest.mark.parametrize("case", _CASES, ids=lambda case: case.id)
def test_plugin_is_redos_safe(case: Case) -> None:
    for filler in _FILLERS:
        md = MarkdownIt("commonmark")
        case.configure(md)
        source = case.payload(filler * _RUN)
        start = time.perf_counter()
        md.render(source)
        elapsed = time.perf_counter() - start
        assert elapsed < _BUDGET_SECONDS, (
            f"{case.id} took {elapsed:.3f}s on a {_RUN}x{filler!r} run; "
            "likely catastrophic backtracking (ReDoS)"
        )
