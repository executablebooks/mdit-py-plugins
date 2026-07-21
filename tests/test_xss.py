"""Categorical XSS guard: render injection probes through each plugin's defaults.

Several plugins register default HTML render rules that interpolate
attacker-controlled token content into markup. Rather than trust review to catch
the next unescaped interpolation, this drives each plugin end-to-end with a probe
and asserts the raw marker never reaches the output (``markdown-it`` runs with raw
HTML disabled, so a correctly-escaped plugin emits ``&lt;xss&gt;`` instead).

Two probe shapes cover the two sinks:

- ``"><xss>`` for HTML/attribute contexts: a plugin that escapes turns the ``<``
  into ``&lt;`` so the ``<xss`` marker disappears; one that doesn't leaks a live
  element (or breaks out of an attribute).
- ``on*`` / ``style`` attribute keys for ``attrs``, where the injection is the
  attribute itself: the default config diverts these to ``token.meta`` so the
  marker is absent from output.

The only per-plugin cost is one activation payload placing the probe where the
plugin captures token content.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from markdown_it import MarkdownIt
import pytest

from mdit_py_plugins.attrs import attrs_block_plugin, attrs_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
from mdit_py_plugins.texmath import texmath_plugin

# A live-element / attribute-breakout probe and the marker that only survives in
# the output if the plugin emitted it without HTML-escaping.
_TAG = '"><xss>'
_TAG_MARKER = "<xss"


@dataclass(frozen=True)
class Case:
    id: str
    configure: Callable[[MarkdownIt], None]
    payload: str
    marker: str


_CASES = [
    Case(
        "texmath-inline-content",
        lambda md: md.use(texmath_plugin),
        f"a ${_TAG}$ b",
        _TAG_MARKER,
    ),
    Case(
        "texmath-block-eqno-info",
        lambda md: md.use(texmath_plugin, delimiters="gitlab"),
        "```math x ``` (<xss onx=1>)",
        "<xss",
    ),
    Case(
        "dollarmath-label",
        lambda md: md.use(dollarmath_plugin),
        f"$$a=1$$ ({_TAG})\n",
        _TAG_MARKER,
    ),
    Case(
        "myst-target",
        lambda md: md.use(myst_block_plugin),
        f"({_TAG})=\n",
        _TAG_MARKER,
    ),
    Case(
        "attrs-span-event",
        lambda md: md.use(attrs_plugin, spans=True),
        '[click]{onxss="alert(1)"}\n',
        "onxss=",
    ),
    Case(
        "attrs-image-event",
        lambda md: md.use(attrs_plugin),
        '![a](img){onxss="alert(1)"}\n',
        "onxss=",
    ),
    Case(
        "attrs-span-style",
        lambda md: md.use(attrs_plugin, spans=True),
        '[click]{style="color:red"}\n',
        "style=",
    ),
    Case(
        "attrs-block-event",
        lambda md: md.use(attrs_block_plugin),
        '{onxss="alert(1)"}\nparagraph\n',
        "onxss=",
    ),
]


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case.id)
def test_plugin_escapes_injection(case: Case) -> None:
    md = MarkdownIt("commonmark")
    case.configure(md)
    out = md.render(case.payload)
    assert case.marker not in out, (
        f"{case.id} emitted {case.marker!r} unescaped: {out!r}"
    )
