"""The plugins that need markdown-it-py >= 4.1.0 refuse older versions.

``test_gfm``, ``test_gfm_autolink`` and ``test_section_ref`` skip below 4.1.0,
so their version guards are tested here, where they run on every supported version
(CI runs the suite on the declared floor, markdown-it-py 3.0.0, as well as the latest).
"""

from types import SimpleNamespace

from markdown_it import MarkdownIt
from markdown_it import __version__ as mdit_version
from packaging.version import Version
import pytest

from mdit_py_plugins.gfm import gfm_plugin
from mdit_py_plugins.gfm_autolink import gfm_autolink_plugin
from mdit_py_plugins.section_ref import section_ref_plugin


@pytest.mark.skipif(
    Version(mdit_version) >= Version("4.1.0"),
    reason="needs markdown-it-py < 4.1.0 installed",
)
@pytest.mark.parametrize(
    "plugin", [gfm_plugin, gfm_autolink_plugin, section_ref_plugin]
)
def test_raises_below_4_1(plugin):
    """On markdown-it-py < 4.1.0 the plugin raises a clear error, not a late failure."""
    with pytest.raises(RuntimeError, match=r"requires markdown-it-py >= 4\.1\.0"):
        MarkdownIt().use(plugin)


def test_section_ref_runtime_error():
    """The plugin requires the ``add_terminator_char`` API (markdown-it-py >= 4.1.0)."""
    md = MarkdownIt()
    md.inline = SimpleNamespace()  # type: ignore[assignment]  # lacks add_terminator_char
    with pytest.raises(RuntimeError, match="requires markdown-it-py"):
        section_ref_plugin(md)
