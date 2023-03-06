# Change Log

## 0.3.5 - 2023-03-02

- 🐛 FIX: Regression in dollarmath by @chrisjsewell in [#69](https://github.com/executablebooks/mdit-py-plugins/pull/69)
- 🐛 Fix regression in amsmath by @chrisjsewell in [#70](https://github.com/executablebooks/mdit-py-plugins/pull/70)
- 🔧 Correct project documentation link by @andersk in [#73](https://github.com/executablebooks/mdit-py-plugins/pull/73)

## 0.3.4 - 2023-02-18

- ✨ NEW: Add attrs_block_plugin by @chrisjsewell in [#66](https://github.com/executablebooks/mdit-py-plugins/pull/66)
- 👌 Improve field lists by @chrisjsewell in [#65](https://github.com/executablebooks/mdit-py-plugins/pull/65)
- 🔧 Update pre-commit by @chrisjsewell in [#64](https://github.com/executablebooks/mdit-py-plugins/pull/64) (moving from flake8 to ruff)

**Full Changelog**: [v0.3.3...v0.3.](https://github.com/executablebooks/mdit-py-plugins/compare/v0.3.3...v0.3.4)

## 0.3.3 - 2022-12-06

🐛 FIX: span with end of inline before attrs

## 0.3.2 - 2022-12-05

- ✨ NEW: Port `admon` plugin by @KyleKing ([#53](https://github.com/executablebooks/mdit-py-plugins/pull/53))
- ✨ NEW: Add span parsing to inline attributes plugin by @chrisjsewell ([#55](https://github.com/executablebooks/mdit-py-plugins/pull/55))
- 🐛 FIX: Task list item marker can be followed by any GFM whitespace by @hukkin in ([#42](https://github.com/executablebooks/mdit-py-plugins/pull/42))

**Full Changelog**: [v0.3.1...v0.4.0](https://github.com/executablebooks/mdit-py-plugins/compare/v0.3.1...v0.4.0)

## 0.3.1 - 2022-09-27

- ⬆️ UPGRADE: Drop Python 3.6, support Python 3.10
- 🐛 FIX: Parsing when newline is between footnote ID and first paragraph
- 🐛 FIX: Anchor ids in separate renders no longer affect each other.
- ✨ NEW: Add `attrs_plugin`
- 🔧 MAINTAIN: Use flit PEP 621 package build

## 0.3.0 - 2021-12-03

- ⬆️ UPGRADE: Compatible with markdown-it-py `v2`.
- ✨ NEW: Add field list plugin, Based on the [restructuredtext syntax](https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#field-lists)
- ♻️ REFACTOR: dollarmath plugin, `math_block_eqno` -> `math_block_label` token
- ♻️ REFACTOR: Remove AttrDict usage from texmath
- 👌 IMPROVE: Default HTML rendering for dollarmath and amsmath plugins
- 👌 IMPROVE: Add render options for dollarmath and amsmath plugins
- 👌 IMPROVE: MyST parsing of target blocks (allow whitespace) and roles (allow for new lines)

## 0.2.8 - 2021-05-03

🐛 FIX: `wordcount` update of minutes

## 0.2.7 - 2021-05-03

- ⬆️ UPDATE: markdown-it-py~=1.0
- ✨ NEW: Add `wordcount_plugin`
- 👌 IMPROVE: `dollarmath`: Allow inline double-dollar
- 👌 IMPROVE: `myst_blocks`: Parse multiline comments
- 👌 IMPROVE: Replace use of `env` as an `AttrDict`
- 🐛 FIX: `front_matter`: don't duplicate content storage in `Token.meta`

## 0.2.6 - 2021-03-17

👌 IMPROVE: Remove direct use of `Token.attrs`

## 0.2.5 - 2021-02-06

🐛 FIX: front-matter: `IndexError` if first line is single dash

## 0.2.2 - 2020-12-16

✨ NEW: Add substitution_plugin
(improvements in 0.2.3 and 0.2.4)

## 0.2.0 - 2020-12-14

Add mypy type-checking, code taken from: https://github.com/executablebooks/markdown-it-py/commit/2eb1fe6b47cc0ad4ebe954cabd91fb8e52a2f03d

## 0.1.0 - 2020-12-14

First release, code taken from: https://github.com/executablebooks/markdown-it-py/commit/3a5bdcc98e67de9df26ebb8bc7cd0221a0d6b51b
