"""Categorical ReDoS guard for every regex shipped by the package.

New plugins add regexes over time. Rather than trust review to catch catastrophic
backtracking, this test discovers every compiled pattern reachable from the
package and asserts it stays fast against adversarial homogeneous input (the
class of input that makes overlapping or nested quantifiers blow up).
"""

from __future__ import annotations

import importlib
import pkgutil
import re
import time

import pytest

import mdit_py_plugins

# Homogeneous runs of a single class of character are what drive overlapping
# quantifiers (e.g. `\s+ [^x]+ \s+`) into super-linear backtracking.
_ADVERSARIAL_CHARS = [" ", "\t", "a", "1", "$", "`", "\\", '"', ".", "-"]
_LENGTH = 20_000
_BUDGET_SECONDS = 0.5

# Metacharacters that end the run of literal leading characters.
_METACHARS = set(".^$*+?()[]{}|")
# Backslash escapes that denote a character *class*, not a literal, so prefix
# extraction must stop rather than emit the letter that follows the backslash.
_CLASS_ESCAPES = set("sSdDwWbBAZ")


def _literal_prefix(source: str) -> str:
    """Best-effort leading literal of a regex, so anchored patterns get exercised.

    Anchored rules like ``^```math\\s+...`` only backtrack once their literal
    lead-in matches, so an adversarial run must be prefixed with that literal.
    Parsing walks the source until the first metacharacter or character class,
    treating ``\\x`` as the literal ``x`` and expanding a ``{n}`` repeat of the
    preceding literal (so ```` `{3} ```` yields three backticks).
    """
    source = source.removeprefix("^")
    out: list[str] = []
    i = 0
    while i < len(source):
        char = source[i]
        if char == "\\" and i + 1 < len(source):
            nxt = source[i + 1]
            if nxt in _CLASS_ESCAPES:
                break
            out.append(nxt)
            i += 2
        elif char == "{" and out:
            end = source.find("}", i)
            count = source[i + 1 : end] if end != -1 else ""
            if not (repeats := count.split(",")[0]).isdigit():
                break
            out.append(out[-1] * (int(repeats) - 1))
            i = end + 1
        elif char in _METACHARS:
            break
        else:
            out.append(char)
            i += 1
    return "".join(out)


def _iter_patterns() -> list[tuple[str, re.Pattern[str]]]:
    found: dict[int, tuple[str, re.Pattern[str]]] = {}

    # Patterns may sit directly in a module global or nested inside a global
    # container (e.g. texmath's ``rules`` dict of delimiter flavors), so recurse.
    def _collect(where: str, value: object) -> None:
        if isinstance(value, re.Pattern):
            found.setdefault(id(value), (where, value))
        elif isinstance(value, dict):
            for item in value.values():
                _collect(where, item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                _collect(where, item)

    for info in pkgutil.walk_packages(
        mdit_py_plugins.__path__, prefix=f"{mdit_py_plugins.__name__}."
    ):
        module = importlib.import_module(info.name)
        for name, value in vars(module).items():
            _collect(f"{info.name}.{name}", value)

    return sorted(found.values(), key=lambda item: item[0])


_PATTERNS = _iter_patterns()

# Several patterns share a ``where`` (e.g. every texmath flavor lives in one
# ``rules`` dict), so include the regex source to keep failing ids unambiguous.
_IDS = [f"{where} {pattern.pattern[:48]}" for where, pattern in _PATTERNS]


@pytest.mark.timeout(10)
@pytest.mark.parametrize("where,pattern", _PATTERNS, ids=_IDS)
def test_regex_is_redos_safe(where: str, pattern: re.Pattern[str]) -> None:
    prefix = _literal_prefix(pattern.pattern)
    for char in _ADVERSARIAL_CHARS:
        payload = prefix + char * _LENGTH
        start = time.perf_counter()
        pattern.search(payload)
        elapsed = time.perf_counter() - start
        assert elapsed < _BUDGET_SECONDS, (
            f"{where} took {elapsed:.3f}s on {prefix!r}+{_LENGTH}x{char!r}; "
            "likely catastrophic backtracking (ReDoS)"
        )


def test_patterns_were_discovered() -> None:
    assert len(_PATTERNS) > 10
