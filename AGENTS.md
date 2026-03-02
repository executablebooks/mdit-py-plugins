# AGENTS.md

This file provides guidance for AI coding agents working on the **mdit-py-plugins** repository.

## Project Overview

mdit-py-plugins is a collection of plugins for [markdown-it-py](https://github.com/executablebooks/markdown-it-py), the Python Markdown parser. It provides:

- Syntax extensions for markdown-it-py (footnotes, front matter, definition lists, task lists, etc.)
- Both block-level and inline-level parsing rules
- Each plugin follows the markdown-it-py plugin architecture: a function that receives a `MarkdownIt` instance and registers rules
- Used extensively by [MyST-Parser](https://github.com/executablebooks/MyST-Parser) for Sphinx documentation

## Repository Structure

```
pyproject.toml          # Project configuration and dependencies (flit)
tox.ini                 # Tox test environment configuration
.pre-commit-config.yaml # Pre-commit hooks configuration

mdit_py_plugins/        # Main source code
├── __init__.py         # Package init (version only)
├── utils.py            # Shared utility functions
├── py.typed            # PEP 561 marker
├── admon/              # Admonition plugin (note, warning, etc.)
├── amsmath/            # AMS math environment plugin
├── anchors/            # Heading anchor plugin
├── attrs/              # Inline/block attribute plugin ({.class #id})
├── colon_fence.py      # Colon fence plugin (:::)
├── container/          # Container plugin (custom divs)
├── deflist/            # Definition list plugin
├── dollarmath/         # Dollar math plugin ($...$, $$...$$)
├── field_list/         # Field list plugin
├── footnote/           # Footnote plugin
├── front_matter/       # YAML front matter plugin
├── myst_blocks/        # MyST block syntax plugin
├── myst_role/          # MyST role syntax plugin ({role}`text`)
├── subscript/          # Subscript plugin (~sub~)
├── substitution.py     # Substitution plugin
├── tasklists/          # Task list plugin (- [x] done)
├── texmath/            # TeX math plugin
└── wordcount/          # Word count plugin

tests/                  # Test suite
├── fixtures/           # Shared test fixture files
├── test_admon/         # Admonition tests with fixture files
├── test_amsmath/       # AMS math tests
├── test_anchors.py     # Anchors tests
├── test_attrs/         # Attributes tests
├── test_colon_fence/   # Colon fence tests
├── test_container/     # Container tests
├── test_deflist/       # Definition list tests
├── test_dollarmath/    # Dollar math tests
├── test_field_list/    # Field list tests
├── test_footnote.py    # Footnote tests
├── test_front_matter.py # Front matter tests
├── test_myst_block.py  # MyST block tests
├── test_myst_role.py   # MyST role tests
├── test_subscript.py   # Subscript tests
├── test_substitution/  # Substitution tests
├── test_tasklists/     # Task list tests
├── test_texmath/       # TeX math tests
└── test_wordcount.py   # Word count tests

docs/                   # Documentation source
├── conf.py             # Sphinx configuration
└── index.md            # Documentation index
```

## Development Commands

All commands should be run via [`tox`](https://tox.wiki) for consistency. The project uses `tox-uv` for faster environment creation.

### Testing

```bash
# Run all tests
tox

# Run tests with specific Python version
tox -e py311

# Run a specific test file
tox -e py310 -- tests/test_footnote.py

# Run a specific test function
tox -e py310 -- tests/test_footnote.py::test_function_name

# Run tests with coverage
tox -e py310 -- --cov=mdit_py_plugins --cov-report=html

# Update regression test fixtures (produces error if files change)
tox -e py310 -- --force-regen
```

### Documentation

```bash
# Build docs (clean)
tox -e docs-clean

# Build docs (incremental)
tox -e docs-update

# Build with a specific builder (e.g., linkcheck to validate external links)
tox -e docs-update -- linkcheck
```

### Code Quality

```bash
# Run all pre-commit hooks (ruff, mypy, trailing whitespace, etc.)
tox -e pre-commit

# Run pre-commit with specific hook
tox -e pre-commit -- --all-files ruff

# Run mypy type checking
tox -e mypy

# Run pre-commit hooks directly (if pre-commit is installed)
pre-commit run --all-files
```

## Code Style Guidelines

- **Formatter/Linter**: Ruff (configured in `pyproject.toml`)
- **Type Checking**: Mypy with strict settings (configured in `pyproject.toml`)
- **Pre-commit**: Use pre-commit hooks for consistent code style

### Best Practices

- **Type annotations**: Use complete type annotations for all function signatures.
- **Docstrings**: Include docstrings for public functions and classes.
- **Pure functions**: Where possible, write pure functions without side effects.
- Follow existing naming conventions (`N802`, `N803`, `N806` are excluded to match markdown-it naming).

## Testing Guidelines

- **Framework**: pytest with `pytest-regressions` for fixture-based tests
- **Fixture pattern**: Most plugins use `.md` fixture files containing input and expected HTML output, separated by `.` markers
- **Test location**: Each plugin has a corresponding test file or directory in `tests/`
- **Regression tests**: Use `pytest-regressions` for comparing rendered output against stored fixtures

### Fixture File Format

Fixture files (`.md` files in test directories) use a specific format:

```markdown
Plugin Name
.
markdown input
.
expected html output
.

Another Test Case
.
more markdown input
.
more expected html output
.
```

### Running Specific Tests

```bash
# Test a single plugin
tox -e py310 -- tests/test_dollarmath.py

# Verbose output with full tracebacks
tox -e py310 -- -v --tb=long tests/test_footnote.py
```

## Architecture

### Plugin Structure

Each plugin follows the markdown-it-py plugin pattern:

```python
from markdown_it import MarkdownIt


def my_plugin(md: MarkdownIt, **options: ...) -> None:
    """My custom plugin description."""
    # Register block rules
    md.block.ruler.before("fence", "my_block_rule", my_block_rule)

    # Register inline rules
    md.inline.ruler.after("emphasis", "my_inline_rule", my_inline_rule)

    # Add render rules
    md.add_render_rule("my_token_type", render_my_token)
```

### Plugin Types

1. **Block plugins** (e.g., `amsmath`, `container`, `deflist`, `front_matter`): Parse block-level syntax using `StateBlock`
2. **Inline plugins** (e.g., `dollarmath`, `myst_role`, `subscript`): Parse inline syntax using `StateInline`
3. **Core plugins** (e.g., `footnote`, `wordcount`): Operate on the full token stream in a post-processing step
4. **Single-file plugins** (e.g., `colon_fence.py`, `substitution.py`): Simple plugins in a single module
5. **Multi-file plugins** (e.g., `footnote/`, `dollarmath/`): More complex plugins with `__init__.py` and `index.py`

### Multi-file Plugin Layout

```
plugin_name/
├── __init__.py   # Exports the plugin function (e.g., dollarmath_plugin)
└── index.py      # Contains the implementation (rule functions, renderers)
```

### Token Flow

Plugins create and manipulate markdown-it tokens:

```python
token = state.push("my_type_open", "div", 1)   # Opening tag
token.attrSet("class", "my-class")
token.markup = "..."
token.map = [startLine, nextLine]

# Content tokens...

token = state.push("my_type_close", "div", -1)  # Closing tag
```

## Commit Message Format

Use this format:

```
<EMOJI> <KEYWORD>: Summarize in 72 chars or less (#<PR>)

Optional detailed explanation.
```

Keywords:

- `✨ NEW:` – New feature
- `🐛 FIX:` – Bug fix
- `👌 IMPROVE:` – Improvement (no breaking changes)
- `‼️ BREAKING:` – Breaking change
- `📚 DOCS:` – Documentation
- `🔧 MAINTAIN:` – Maintenance changes only (typos, etc.)
- `🧪 TEST:` – Tests or CI changes only
- `♻️ REFACTOR:` – Refactoring

## Pull Request Requirements

When submitting changes:

1. **Description**: Include a meaningful description or link explaining the change
2. **Tests**: Include test cases for new functionality or bug fixes
3. **Documentation**: Update docs if behavior changes or new features are added
4. **Changelog**: Update `CHANGELOG.md` under the appropriate section
5. **Code Quality**: Ensure `pre-commit run --all-files` passes
6. **Type Checking**: Ensure mypy passes with strict settings

## Key Files

- `pyproject.toml` - Project configuration, dependencies, and tool settings (Ruff, Mypy)
- `tox.ini` - Test environment configuration
- `mdit_py_plugins/__init__.py` - Package version
- `mdit_py_plugins/utils.py` - Shared utilities (e.g., `is_code_block`)
- `CHANGELOG.md` - Change log for releases

## Debugging

- Use `md.parse(text)` to inspect the token stream produced by plugins
- Use `md.render(text)` to see final HTML output
- Enable/disable specific plugins using `md.use()` / `md.disable()`
- Use `tox -- -v --tb=long` for verbose test output with full tracebacks

### Debugging Tips

```python
from markdown_it import MarkdownIt

from mdit_py_plugins.dollarmath import dollarmath_plugin

md = MarkdownIt().use(dollarmath_plugin)

# See the token stream
tokens = md.parse("Some $inline$ math and $$block$$ math")
for token in tokens:
    print(f"{token.type} | {token.tag} | {token.content}")
    if token.children:
        for child in token.children:
            print(f"  {child.type} | {child.tag} | {child.content}")

# See rendered HTML
print(md.render("Some $inline$ math"))
```

## Common Patterns

### Adding a New Plugin

1. Create a new directory under `mdit_py_plugins/` (or a single `.py` file for simple plugins)
2. Implement the plugin function following the standard pattern:
   ```python
   from markdown_it import MarkdownIt

   def my_plugin(md: MarkdownIt) -> None:
       md.block.ruler.before("fence", "my_rule", _my_rule)
       md.add_render_rule("my_type", _render_my_type)
   ```
3. Export the plugin function from `__init__.py`
4. Add test fixtures in `tests/test_my_plugin/`
5. Add a test file `tests/test_my_plugin.py`
6. Update `CHANGELOG.md`

### Adding a Block Rule

Block rules receive `(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool`:

```python
from markdown_it.rules_block import StateBlock

def my_block_rule(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    # Check if this line matches your syntax
    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    if state.src[pos] != "$":
        return False

    # In silent mode, just return True if matched (used for validation)
    if silent:
        return True

    # Parse content and create tokens
    token = state.push("my_type", "", 0)
    token.content = ...
    token.map = [startLine, nextLine]

    state.line = nextLine
    return True
```

### Adding an Inline Rule

Inline rules receive `(state: StateInline, silent: bool) -> bool`:

```python
from markdown_it.rules_inline import StateInline

def my_inline_rule(state: StateInline, silent: bool) -> bool:
    if state.src[state.pos] != "$":
        return False

    # Parse and validate
    ...

    if not silent:
        token = state.push("my_type", "", 0)
        token.content = content

    state.pos = end
    return True
```

## Reference Documentation

- [markdown-it-py Documentation](https://markdown-it-py.readthedocs.io/)
- [markdown-it-py Repository](https://github.com/executablebooks/markdown-it-py)
- [mdit-py-plugins Documentation](https://mdit-py-plugins.readthedocs.io/)
- [Original markdown-it (JavaScript)](https://github.com/markdown-it/markdown-it)
- [CommonMark Spec](https://spec.commonmark.org/)
- [MyST-Parser Repository](https://github.com/executablebooks/MyST-Parser)
