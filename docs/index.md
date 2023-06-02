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

The [`mdit_py_plugins`](https://github.com/executablebooks/mdit-py-plugins), contains a number of common plugins.
They can be chained and loaded *via*:

```python
from markdown_it import MarkdownIt
from mdit_py_plugins import plugin1, plugin2
md = MarkdownIt().use(plugin1, keyword=value).use(plugin2, keyword=value)
html_string = md.render("some *Markdown*")
```

## Front-Matter

```{eval-rst}
.. autofunction:: mdit_py_plugins.front_matter.front_matter_plugin
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
.. autofunction:: mdit_py_plugins.dollarmath.dollarmath_plugin
```

```{eval-rst}
.. autofunction:: mdit_py_plugins.amsmath.amsmath_plugin
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

- [subscript](https://github.com/markdown-it/markdown-it-sub)
- [superscript](https://github.com/markdown-it/markdown-it-sup)
- [abbreviation](https://github.com/markdown-it/markdown-it-abbr)
- [emoji](https://github.com/markdown-it/markdown-it-emoji)
- [insert](https://github.com/markdown-it/markdown-it-ins)
- [mark](https://github.com/markdown-it/markdown-it-mark)
- ... and [others](https://www.npmjs.org/browse/keyword/markdown-it-plugin)
