"""XSS guard: render injection probes through plugins' default renderers (#143).

Several plugins register default HTML render rules that interpolate
attacker-controlled token content into markup. Rather than trust review to catch
the next unescaped interpolation, this drives each covered plugin end-to-end
with a probe and asserts the raw marker never reaches the output.

markdown-it is built with ``html=False``: the ``commonmark`` preset allows raw
HTML, which would pass the probes through core rules rather than a plugin.
Each case also states text the output must contain, which shows that the probe
reached the plugin's renderer (a payload the plugin does not parse would pass
the marker check without testing anything).

Three probe shapes cover the sinks:

- ``"><xss>`` for element and attribute contexts: a plugin that escapes turns
  the ``<`` into ``&lt;``, so the ``<xss`` marker disappears; one that doesn't
  leaks a live element (or breaks out of an attribute).
- ``a" onxss="1`` for attribute contexts: the quote-only breakout, which has
  no ``<`` for the first probe to catch; escaped, ``onxss="`` disappears.
- attribute keys and values for ``attrs``, where the injection is the
  attribute itself: ``on*`` keys, and ``javascript:`` URLs in ``href``.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from markdown_it import MarkdownIt
import pytest

from mdit_py_plugins.attrs import attrs_block_plugin, attrs_plugin
from mdit_py_plugins.colon_fence import colon_fence_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.myst_blocks import myst_block_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.texmath import texmath_plugin

# A live-element / attribute-breakout probe and the marker that only survives in
# the output if the plugin emitted it without HTML-escaping.
_TAG = '"><xss>'
_TAG_MARKER = "<xss"
_TAG_ESCAPED = "&quot;&gt;&lt;xss&gt;"
# A quote-only attribute breakout probe, and its marker.
_QUOTE = 'a" onxss="1'
_QUOTE_MARKER = 'onxss="'


@dataclass(frozen=True)
class Case:
    id: str
    configure: Callable[[MarkdownIt], None]
    payload: str
    marker: str
    reached: str
    """Text in the output showing the probe reached the plugin's renderer."""


_CASES = [
    Case(
        "texmath-inline-content",
        lambda md: md.use(texmath_plugin),
        f"a ${_TAG}$ b",
        _TAG_MARKER,
        f"<eq>{_TAG_ESCAPED}</eq>",
    ),
    Case(
        "dollarmath-label",
        lambda md: md.use(dollarmath_plugin),
        f"$$a=1$$ ({_TAG})\n",
        _TAG_MARKER,
        f'<div id="{_TAG_ESCAPED}" class="math block">',
    ),
    Case(
        "dollarmath-label-quote",
        lambda md: md.use(dollarmath_plugin),
        f"$$a=1$$ ({_QUOTE})\n",
        _QUOTE_MARKER,
        '<div id="a&quot;-onxss=&quot;1" class="math block">',
    ),
    Case(
        "myst-target",
        lambda md: md.use(myst_block_plugin),
        f"({_TAG})=\n",
        _TAG_MARKER,
        f'<a href="#{_TAG_ESCAPED}">',
    ),
    Case(
        "myst-target-quote",
        lambda md: md.use(myst_block_plugin),
        f"({_QUOTE})=\n",
        _QUOTE_MARKER,
        '<a href="#a&quot; onxss=&quot;1">',
    ),
    Case(
        "colon-fence-name",
        lambda md: md.use(colon_fence_plugin),
        f":::a{_TAG}\nx\n:::\n",
        _TAG_MARKER,
        f'<code class="block-a{_TAG_ESCAPED}" >',
    ),
    Case(
        "colon-fence-name-quote",
        # the block name ends at the first space, so the probe has none
        lambda md: md.use(colon_fence_plugin),
        ':::a"onxss="1\nx\n:::\n',
        _QUOTE_MARKER,
        '<code class="block-a&quot;onxss=&quot;1" >',
    ),
    Case(
        "tasklists-label-after",
        lambda md: md.use(tasklists_plugin, label=True, label_after=True),
        f"- [ ] {_TAG}\n",
        _TAG_MARKER,
        f" {_TAG_ESCAPED}</label>",
    ),
    Case(
        "attrs-span-event",
        lambda md: md.use(attrs_plugin, spans=True),
        '[click]{onxss="alert(1)"}\n',
        "onxss=",
        "<p><span>click</span></p>",
    ),
    Case(
        "attrs-image-event",
        lambda md: md.use(attrs_plugin),
        '![a](img){onxss="alert(1)"}\n',
        "onxss=",
        '<p><img src="img" alt="a"></p>',
    ),
    Case(
        "attrs-block-event",
        lambda md: md.use(attrs_block_plugin),
        '{onxss="alert(1)"}\nparagraph\n',
        "onxss=",
        "<p>paragraph</p>",
    ),
    Case(
        "attrs-link-href-url",
        lambda md: md.use(attrs_plugin),
        '[a](https://x){href="javascript:alert(1)"}\n',
        "javascript:",
        '<p><a href="https://x">a</a></p>',
    ),
]


def _md() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": False})
    md.options["xhtmlOut"] = False
    return md


@pytest.mark.parametrize("case", _CASES, ids=lambda case: case.id)
def test_plugin_escapes_injection(case: Case) -> None:
    md = _md()
    case.configure(md)
    out = md.render(case.payload)
    assert case.marker not in out, (
        f"{case.id} emitted {case.marker!r} unescaped: {out!r}"
    )
    assert case.reached in out, f"{case.id} did not reach the renderer: {out!r}"


@pytest.mark.xfail(
    strict=True,
    reason="texmath never renders equation numbers: its render rules close over "
    "the loop variable (# noqa: B023), so every block uses the last template",
)
def test_texmath_eqno_label_escaped() -> None:
    """The texmath equation number is escaped when it is rendered.

    It is not rendered today, so this fails; when that bug is fixed it passes,
    and ``strict`` turns the unexpected pass red so this marker is removed.
    """
    md = _md().use(texmath_plugin, delimiters="gitlab")
    src = f"```math x ``` ({_TAG})"
    assert [t.type for t in md.parse(src)] == ["math_block_eqno"]
    out = md.render(src)
    assert _TAG_MARKER not in out
    assert _TAG_ESCAPED in out
