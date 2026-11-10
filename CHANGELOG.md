# Change Log

## 0.7.0 - 2026-11-10

A security and bug-fix release.
Plugin renderers now escape user content in HTML attribute, label and math positions,
`attrs` drops event-handler attributes by default and validates URL-valued attributes,
and the regular expressions in `texmath` ```` ```math ```` blocks and `admon` headers no longer backtrack polynomially (#143).
It also fixes parser hangs in `gfm_autolink` (#160) and `texmath` (#156),
and adds the `section_ref` plugin;
it requires markdown-it-py >= 3.0 and supports Python 3.10 to 3.14.
Several fixes change rendered output: see **Upgrade notes** below.

### Upgrade notes

- **Requires markdown-it-py >= 3.0** ([#170](https://github.com/executablebooks/mdit-py-plugins/pull/170)).
  The declared floor was 2.0, but 0.5.0 and later already failed to import `subscript` with markdown-it-py 2.x.
  `section_ref`, `gfm` and `gfm_autolink` still need markdown-it-py >= 4.1 and raise `RuntimeError` on older versions.
  Python 3.10 to 3.14 are supported.

- **`attrs_plugin` / `attrs_block_plugin` defaults are stricter** ([#150](https://github.com/executablebooks/mdit-py-plugins/pull/150)).
  With no `allowed` list, event-handler attributes (any key starting with `on`, in any case) are removed
  and moved to `token.meta["insecure_attrs"]`; `style` is kept.
  Whatever `allowed` says, `href`, `src`, `action`, `formaction` and `xlink:href` are removed when `md.validateLink` rejects their value,
  so `[a](https://x){href="javascript:alert(1)"}` keeps `href="https://x"`.
  Text spans (`[text]{...}`) now honour `allowed`, which they used to bypass.
  This is a baseline, not a sanitiser: for untrusted input, pass an explicit list such as `allowed=("id", "class")`.
- **Renderers escape their output** ([#150](https://github.com/executablebooks/mdit-py-plugins/pull/150), [#165](https://github.com/executablebooks/mdit-py-plugins/pull/165)).
  The `texmath` default renderer HTML-escapes the math source (`$a<b$` now renders `<eq>a&lt;b</eq>`),
  and the `dollarmath` equation label, the `myst_block` target label, the `colon_fence` class name
  and the `tasklists` `label_after` label are escaped too.
  Benign text containing `&`, `<`, `>` or `"` in these positions is now emitted as entities.
- **`anchors_plugin` ids can change** ([#159](https://github.com/executablebooks/mdit-py-plugins/pull/159)).
  An explicit heading id (such as `{#custom}` from `attrs_block_plugin`) is now kept instead of being overwritten,
  and generated slugs avoid it.
  The default slug function no longer strips whitespace from the title,
  matching MyST-Parser's `github_slugify`:
  a title that starts or ends with a space next to an image, raw HTML or an entity gets a different id
  (`# Foo ![img](x.png)` now gives `foo-`, it was `foo`).
  To keep the old ids, pass `slug_func=lambda title: slugify(title.strip())`, with `slugify` from `mdit_py_plugins.anchors.index`.
- **`mdit_py_plugins.attrs.parse.parse()` raises on an unterminated attribute group**, instead of succeeding at the end of the string
  ([#153](https://github.com/executablebooks/mdit-py-plugins/pull/153)).
  Every plugin call site declines the group, so `` `a`{.a `` now renders `<code>a</code>{.a`; it used to drop the `{.a`.
- **The `section_ref` token shape is public API** ([#169](https://github.com/executablebooks/mdit-py-plugins/pull/169)): see its entry below.

### 🔒 Security

Thanks to [@KrisKennawayDD](https://github.com/KrisKennawayDD) for reporting these issues in #143,
and to [@KyleKing](https://github.com/KyleKing) for the ReDoS analysis and fixes.

- 🔒 FIX: Escape plugin renderer output and harden the `attrs` defaults, thanks to [@KyleKing](https://github.com/KyleKing) for the cross-plugin XSS test ([#150](https://github.com/executablebooks/mdit-py-plugins/pull/150), folding in [#151](https://github.com/executablebooks/mdit-py-plugins/pull/151))

  With markdown-it-py's `html` option off, untrusted Markdown could still inject HTML or script through:
  the `texmath` default renderer (math source), the `dollarmath` equation label (`id` and permalink `href`),
  the `myst_block` `(name)=` target label, and `attrs` / `attrs_block` event-handler and `javascript:` URL attributes.
  All of these are now escaped or filtered (see **Upgrade notes**),
  and `tests/test_xss.py` renders injection probes through each plugin's default renderer.

- 🔒 FIX: Escape the `colon_fence` class name and the `tasklists` `label_after` label ([#165](https://github.com/executablebooks/mdit-py-plugins/pull/165))

  `:::a"onmouseover="alert(1)` rendered an attribute-breaking `class="block-a"onmouseover="alert(1)"`,
  and `- [ ] <img src=x onerror=alert(1)>` with `label=True, label_after=True` rendered a raw `<img>`.

- 🔒 FIX: ReDoS in `texmath` ```` ```math ```` blocks and `admon` headers, thanks to [@KyleKing](https://github.com/KyleKing) ([#148](https://github.com/executablebooks/mdit-py-plugins/pull/148))

  The `texmath` ```` ```math ```` patterns (the `gitlab` and `julia` delimiters) backtracked cubically
  on a fence followed by a long whitespace run with no closing fence,
  and the `admon` multi-tag title pattern backtracked quadratically on a header with a long run of spaces or double quotes.
  Both now run in linear time and match what they matched before, so output is unchanged.

### ✨ New

- ✨ NEW: Add the section reference plugin (`section_ref`) ([#144](https://github.com/executablebooks/mdit-py-plugins/pull/144), [#168](https://github.com/executablebooks/mdit-py-plugins/pull/168), [#169](https://github.com/executablebooks/mdit-py-plugins/pull/169))

  The `section_ref` plugin captures section-sign references, the syntax LLMs
  commonly use to point at numbered headings, into dedicated `section_ref` tokens,
  so downstream renderers (e.g. MyST-Parser) can resolve them to heading cross-references:

  ```markdown
  See §1, §1.1 and §2.3.4 for details.
  ```

  A `§` must be immediately followed by one or more `.`-separated levels of 1 to 9 ASCII digits, with no spaces.
  A trailing `.` is not part of the reference, and a reference directly followed by an ASCII letter (`§1a`),
  or with a level longer than nine digits, stays literal text.
  Each reference is a `section_ref` leaf token whose `content` is the text as written
  and whose `meta["numbers"]` lists each level as an int (e.g. `[1, 1]` for `§1.1`).
  The grammar and the token shape are documented in the plugin docstring and are public API from this release.
  It renders as `<span class="section-ref">§1.1</span>` by default.

  **Requires markdown-it-py >= 4.1.0.**

### 🐛 Fixes

- 🐛 FIX: `gfm_autolink` no longer hangs on autolink-like text in link labels (#160), thanks to [@AryanRG](https://github.com/AryanRG) ([#161](https://github.com/executablebooks/mdit-py-plugins/pull/161))
- 🐛 FIX: `texmath` no longer loops forever on block math opened in a blockquote and closed after it (#156), thanks to [@acaprino](https://github.com/acaprino) ([#157](https://github.com/executablebooks/mdit-py-plugins/pull/157))
- 🐛 FIX: `dollarmath`: a same-line `$$…$$` followed by text no longer swallows the following lines (#147), thanks to [@KyleKing](https://github.com/KyleKing) ([#149](https://github.com/executablebooks/mdit-py-plugins/pull/149))
- 🐛 FIX: `dollarmath`: multi-line `$$` blocks in a blockquote no longer keep the `>` prefixes in their content (#125), thanks to [@BetterAndBetterII](https://github.com/BetterAndBetterII) ([#152](https://github.com/executablebooks/mdit-py-plugins/pull/152))
- 🐛 FIX: `front_matter`: parse front matter closed by the YAML `...` document-end marker, thanks to [@feiiiiii5](https://github.com/feiiiiii5) ([#158](https://github.com/executablebooks/mdit-py-plugins/pull/158))

  A block whose last line was `...` used to leak into the document as text.
  The marker must be at column 0 and may be followed by spaces only.

- 🐛 FIX: `footnote`: reserve an inline footnote's id before parsing its content, thanks to [@civilwarinfrance](https://github.com/civilwarinfrance) ([#162](https://github.com/executablebooks/mdit-py-plugins/pull/162))

  A `[^named]` reference or a nested `^[...]` inside an inline footnote no longer loses the inner note, duplicates an id, or raises `KeyError: 'count'`.

- 🐛 FIX: `anchors`: keep explicit heading ids, and do not strip slug titles, thanks to [@muneikh](https://github.com/muneikh) ([#159](https://github.com/executablebooks/mdit-py-plugins/pull/159))
- 🐛 FIX: `attrs`: unterminated groups, class accumulation and closing-token merge ([#153](https://github.com/executablebooks/mdit-py-plugins/pull/153))

  An unterminated attribute group no longer swallows the text after it.
  Classes from adjacent attribute groups are combined on spans and links (`[a]{.x}{.y}` gives `class="x y"`),
  as they already were on inline code and images.
  An attributes block at the end of a container is no longer merged onto the closing token
  (`> {.a}` rendered `</blockquote class="a">`).

- 🐛 FIX: `myst_role` no longer rejects a role at the start of inline content when the content ends with a backslash,
  and `` \\{name}`x` `` (an escaped backslash before a role) now parses the role (#62) ([#145](https://github.com/executablebooks/mdit-py-plugins/pull/145))

### 📚 Documentation

- 📚 DOCS: Explain front matter extraction and HTML rendering (#133), thanks to [@Gonghan-Princess](https://github.com/Gonghan-Princess) ([#154](https://github.com/executablebooks/mdit-py-plugins/pull/154))
- 📚 DOCS: A runnable usage example (#44), the `dollarmath` rendering contract and a "Rendering dollarmath output" guide (#111),
  and Read the Docs builds on Python 3.13 ([#166](https://github.com/executablebooks/mdit-py-plugins/pull/166))

### 🔧 Maintenance

- 🔧 Require markdown-it-py >= 3.0, test the floor and Python 3.14 in CI, and update the classifiers ([#170](https://github.com/executablebooks/mdit-py-plugins/pull/170))
- 🔧 Releases are published to PyPI with trusted publishing (#141), with attestations ([#142](https://github.com/executablebooks/mdit-py-plugins/pull/142)),
  from distributions built with `python -m build` and checked on every pull request ([#164](https://github.com/executablebooks/mdit-py-plugins/pull/164))
- 🔧 pre-commit autoupdate (ruff 0.17, mypy 2.4) with a pinned ruff base rule set ([#138](https://github.com/executablebooks/mdit-py-plugins/pull/138)),
  and a non-blocking Codecov upload ([#167](https://github.com/executablebooks/mdit-py-plugins/pull/167))

**Full Changelog**: <https://github.com/executablebooks/mdit-py-plugins/compare/v0.6.1...v0.7.0>

## 0.6.1 - 2026-05-13

- 🐛 FIX: Nested field lists incorrectly nesting inside parent containers (#139)

  Field lists inside list items (or other indented containers) would recursively nest each field inside the previous one, instead of being siblings.

## 0.6.0 - 2026-05-07

- ✨ NEW: Add GFM autolink and composite GFM plugins (#135)

  The `gfm_autolink` plugin implements [GFM autolink literals](https://github.github.com/gfm/#autolinks-extension-),
  auto-linking URLs and email addresses without requiring angle brackets:

  ```markdown
  Visit www.example.com or contact user@example.com
  ```

  The `gfm` composite plugin enables a full Github Flavored Markdown (GFM)-like configuration in a single call
  (tables, strikethrough, autolinks, task lists, alerts, and footnotes).

  See [the GitHub docs](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) for more information.

  **Requires markdown-it-py >= 4.1.0.**

- ✨ NEW: Add superscript plugin and tests, thanks to @elijahgreenstein (#128)

  Ported from [markdown-it-sup](https://github.com/markdown-it/markdown-it-sup).
  Renders superscript text using `^..^` syntax:

  ```markdown
  29^th^ of May
  ```

## 0.5.0 - 2025-08-11

- ⬆️ Drop Python 3.9, which is EoL next month <https://devguide.python.org/versions> and allow for the, soon to be released, markdown-it-py v4.
- ✨ NEW: Add plugin & tests to render subscripts, thanks to @miteshashar

## 0.4.2 - 2024-09-09

- 👌 Improve parsing of nested amsmath

  The previous logic was problematic for amsmath blocks nested in other blocs (such as blockquotes)

  The new parsing code now principally follows the logic in `markdown_it/rules_block/fence.py`
  (see also <https://spec.commonmark.org/0.30/#fenced-code-blocks>),
  except that:

  1. it allows for a closing tag on the same line as the opening tag, and
  2. it does not allow for an opening tag without closing tag (i.e. no auto-closing)

- ✨ Add `allowed` option for inline/block attributes

  The `allowed` option accepts a list of allowed attribute names.
  If not ``None``, any attributes not in this list will be removed
  and placed in the token's meta under the key `"insecure_attrs"`.

## 0.4.1 - 2024-05-12

* 👌 Add option for footnotes references to always be matched

  Usually footnote references are only matched when a footnote definition of the same label has already been found. If `always_match_refs=True`, any `[^...]` syntax will be treated as a footnote.

## 0.4.0 - 2023-06-05

* ⬆️ UPGRADE: Drop python 3.7 and support 3.11 ([#77](https://github.com/executablebooks/mdit-py-plugins/pull/77))

* ⬆️ UPGRADE: Allow markdown-it-py v3 ([#85](https://github.com/executablebooks/mdit-py-plugins/pull/85))
  * 👌 Make field_list compatible with latest upstream ([#75](https://github.com/executablebooks/mdit-py-plugins/pull/75))
  * 🔧 Convert `state.srcCharCode` -> `state.src` ([#84](https://github.com/executablebooks/mdit-py-plugins/pull/84))
  * 🔧 Remove unnecessary method arg by @chrisjsewell in( [#76](https://github.com/executablebooks/mdit-py-plugins/pull/76))
  * 👌 Centralise code block test ([#83](https://github.com/executablebooks/mdit-py-plugins/pull/83) and [#87](https://github.com/executablebooks/mdit-py-plugins/pull/87))
    * This means that disabling the `code` block rule in markdown-it-py v3+ will now allow all syntax blocks to be indented by any amount of whitespace.

* 👌 Improve `dollarmath` plugin: Add `allow_blank_lines` option, thanks to [@eric-wieser](https://github.com/eric-wieser) ([#46](https://github.com/executablebooks/mdit-py-plugins/pull/46))

* 👌 Improve `admon` plugin: Add `???` support, thanks to [@KyleKing](https://github.com/KyleKing) ([#58](https://github.com/executablebooks/mdit-py-plugins/pull/58))

* 🔧 MAINTAIN: Make type checking strict ([#86](https://github.com/executablebooks/mdit-py-plugins/pull/86))

**Full Changelog**: <https://github.com/executablebooks/mdit-py-plugins/compare/v0.3.5...v0.4.0>

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
