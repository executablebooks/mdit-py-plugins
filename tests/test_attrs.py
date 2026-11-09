from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.utils import read_fixture_file
import pytest

from mdit_py_plugins.attrs import attrs_block_plugin, attrs_plugin
from mdit_py_plugins.attrs.parse import ParseError, parse

FIXTURE_PATH = Path(__file__).parent.joinpath("fixtures")


@pytest.mark.parametrize(
    "line,title,input,expected", read_fixture_file(FIXTURE_PATH / "attrs.md")
)
def test_attrs(line, title, input, expected):
    md = MarkdownIt("commonmark").use(attrs_plugin, spans=True).use(attrs_block_plugin)
    if "DISABLE-CODEBLOCKS" in title:
        md.disable("code")
    md.options["xhtmlOut"] = False
    text = md.render(input)
    print(text)
    assert text.rstrip() == expected.rstrip()


def test_attrs_allowed(data_regression):
    allowed = ["safe"]
    md = (
        MarkdownIt("commonmark")
        .use(attrs_plugin, allowed=allowed)
        .use(attrs_block_plugin, allowed=allowed)
    )
    tokens = md.parse("""
{danger1=a safe=b}
{danger2=c safe=d}
# header

`inline`{safe=a danger=b}
    """)
    data_regression.check([t.as_dict() for t in tokens])


class _ScanCountingStr(str):
    """A string that counts the characters its scanning methods could visit.

    Slicing counts the length of the slice;
    the substring and search methods count the whole string (an upper bound).
    """

    scanned = 0

    def __getitem__(self, key):
        result = super().__getitem__(key)
        _ScanCountingStr.scanned += len(result)
        return result

    def __contains__(self, key):
        _ScanCountingStr.scanned += len(self)
        return super().__contains__(key)

    def find(self, *args):
        _ScanCountingStr.scanned += len(self)
        return super().find(*args)

    def rfind(self, *args):
        _ScanCountingStr.scanned += len(self)
        return super().rfind(*args)

    def index(self, *args):
        _ScanCountingStr.scanned += len(self)
        return super().index(*args)

    def rindex(self, *args):
        _ScanCountingStr.scanned += len(self)
        return super().rindex(*args)

    def count(self, *args):
        _ScanCountingStr.scanned += len(self)
        return super().count(*args)


@pytest.mark.parametrize("n", [1_000, 4_000])
@pytest.mark.parametrize(
    "tail,accepted",
    [
        pytest.param("%", False, id="unterminated"),
        pytest.param("%}", True, id="terminated"),
    ],
)
def test_comment_brace_scan_is_linear(n, tail, accepted):
    """A `}` inside a comment must not rescan the rest of the string.

    Whether a `}` ends a comment depends on whether a `%` follows it.
    Searching the rest of the string at every `}` is quadratic,
    which an input such as `{%` + `}` * n + `%` turns into a hang.
    Count the characters scanned, rather than timing, so the test is deterministic:
    a linear parse scans a small multiple of the length at any n.
    """
    text = _ScanCountingStr("{%" + "}" * n + tail)
    _ScanCountingStr.scanned = 0
    if accepted:
        assert parse(text) == (len(text) - 1, {})
    else:
        with pytest.raises(ParseError, match="not terminated"):
            parse(text)
    assert _ScanCountingStr.scanned <= 10 * len(text)
