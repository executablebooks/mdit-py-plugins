# Markdown-It-Py Plugin Extensions

## Built-in

The following plugins are embedded within the core package:

- [tables](https://help.github.com/articles/organizing-information-with-tables/) (GFM)
- [strikethrough](https://help.github.com/articles/basic-writing-and-formatting-syntax/#styling-text) (GFM)

These can be enabled individually:

```python
from markdown_it import MarkdownIt
md = MarkdownIt("commonmark").enable('table')
```

or as part of a configuration:

```python
from markdown_it import MarkdownIt
md = MarkdownIt("gfm-like")
```

```{seealso}
See <inv:markdown_it#using>
```

## mdit-py-plugins package

The [`mdit_py_plugins`](https://github.com/executablebooks/mdit-py-plugins) package contains a number of common plugins.
Each plugin is a function in its own submodule (for example `mdit_py_plugins.footnote.footnote_plugin`),
so import it from there; the top-level package does not re-export them.

Load a plugin with `MarkdownIt.use`, passing any options as keyword arguments.
`use` returns the `MarkdownIt` instance, so the calls can be chained:

```python
from markdown_it import MarkdownIt
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

md = (
    MarkdownIt("commonmark")
    .use(front_matter_plugin)
    .use(footnote_plugin)
    .use(tasklists_plugin, enabled=True)
)
text = """\
---
title: Example
---
- [x] Some *Markdown*[^1]

[^1]: A footnote.
"""
html_string = md.render(text)
```

The options of each plugin are listed in its section below.

## Front-Matter

```{eval-rst}
.. autofunction:: mdit_py_plugins.front_matter.front_matter_plugin
```

## GFM (GitHub Flavored Markdown)

```{eval-rst}
.. autofunction:: mdit_py_plugins.gfm.gfm_plugin
```

## GFM Autolinks

```{eval-rst}
.. autofunction:: mdit_py_plugins.gfm_autolink.gfm_autolink_plugin
```

## Footnotes

```{eval-rst}
.. autofunction:: mdit_py_plugins.footnote.footnote_plugin
```

## Definition Lists

```{eval-rst}
.. autofunction:: mdit_py_plugins.deflist.deflist_plugin
```

## Task lists

```{eval-rst}
.. autofunction:: mdit_py_plugins.tasklists.tasklists_plugin
```

## Field Lists

```{eval-rst}
.. autofunction:: mdit_py_plugins.field_list.fieldlist_plugin
```

## Heading Anchors

```{eval-rst}
.. autofunction:: mdit_py_plugins.anchors.anchors_plugin
```

## Word Count

```{eval-rst}
.. autofunction:: mdit_py_plugins.wordcount.wordcount_plugin
```

## Containers

```{eval-rst}
.. autofunction:: mdit_py_plugins.container.container_plugin
```

```{eval-rst}
.. autofunction:: mdit_py_plugins.admon.admon_plugin
```

## Attributes

```{eval-rst}
.. autofunction:: mdit_py_plugins.attrs.attrs_plugin
```

```{eval-rst}
.. autofunction:: mdit_py_plugins.attrs.attrs_block_plugin
```

## Math

```{eval-rst}
.. autofunction:: mdit_py_plugins.texmath.texmath_plugin
```

```{eval-rst}
.. autofunction:: mdit_py_plugins.amsmath.amsmath_plugin
```

```{eval-rst}
.. autofunction:: mdit_py_plugins.dollarmath.dollarmath_plugin
```

### Rendering dollarmath output

`dollarmath_plugin` does not typeset math: it wraps each piece of math in an HTML element, listed above.
The tag says how to display the math, and the class says where it was written.
So inline `$$x$$` (with `double_inline=True`) becomes `<div class="math inline">`:
display math written inside a paragraph.
Pick the display mode from the tag (`div` or `span`), not from the class.

There are two common ways to typeset the output.

**Add delimiters on the server, with `renderer=`.**
The `renderer` function receives the math content and `{"display_mode": bool}`,
and returns the HTML to put inside the element.
Wrapping the content in `\(...\)` or `\[...\]` lets MathJax (with its default configuration)
or KaTeX's auto-render extension find it in the page:

```python
from markdown_it import MarkdownIt
from markdown_it.common.utils import escapeHtml
from mdit_py_plugins.dollarmath import dollarmath_plugin


def render_tex(content: str, options: dict) -> str:
    content = escapeHtml(content)
    if options["display_mode"]:
        return rf"\[{content}\]"
    return rf"\({content}\)"


md = MarkdownIt().use(dollarmath_plugin, double_inline=True, renderer=render_tex)
html_string = md.render("Inline $a<b$ and $$x^2$$ in a paragraph.")
```

which gives:

```html
<p>Inline <span class="math inline">\(a&lt;b\)</span> and <div class="math inline">\[x^2\]</div> in a paragraph.</p>
```

A browser closes the `<p>` before the `<div>`, so in the page the text after inline `$$...$$`
falls outside the paragraph: allow for that when styling or selecting this output.

The returned string is inserted as is, so escape the content, as above, unless it comes from a trusted source
(the default renderer escapes it for you).
The same function can instead return fully typeset output, such as MathML from a converter library.

**Typeset the elements in the browser.**
Without a `renderer`, each element holds the escaped LaTeX source,
and a script can typeset the elements in place, for example with KaTeX:

```javascript
for (const el of document.querySelectorAll("span.math, div.math")) {
  // a labelled block starts with its permalink anchor: keep it out of the math
  const label = el.querySelector(".mathlabel");
  if (label) label.remove();
  katex.render(el.textContent.trim(), el, {
    displayMode: el.tagName === "DIV",
    throwOnError: false,
  });
  if (label) el.prepend(label);
}
```

To change the label anchor, pass `label_renderer=`.
To change the tags or classes themselves, replace the render rule for a token type
with `md.add_render_rule` after loading the plugin.

## Subscripts

```{eval-rst}
.. autofunction:: mdit_py_plugins.subscript.sub_plugin
```

## Superscript

```{eval-rst}
.. autofunction:: mdit_py_plugins.superscript.superscript_plugin
```

## Section References

```{eval-rst}
.. autofunction:: mdit_py_plugins.section_ref.section_ref_plugin
```

## MyST plugins

`myst_blocks` and `myst_role` plugins are also available, for utilisation by the [MyST renderer](https://myst-parser.readthedocs.io/en/latest/using/syntax.html)

```{eval-rst}
.. autofunction:: mdit_py_plugins.myst_role.myst_role_plugin
.. autofunction:: mdit_py_plugins.myst_blocks.myst_block_plugin
```

## Write your own

Use the `mdit_py_plugins` as a guide to write your own, following the [markdown-it design principles](inv:markdown_it#architecture).

There are many other plugins which could easily be ported from the JS versions (and hopefully will):

- [abbreviation](https://github.com/markdown-it/markdown-it-abbr)
- [emoji](https://github.com/markdown-it/markdown-it-emoji)
- [insert](https://github.com/markdown-it/markdown-it-ins)
- [mark](https://github.com/markdown-it/markdown-it-mark)
- ... and [others](https://www.npmjs.org/browse/keyword/markdown-it-plugin)
