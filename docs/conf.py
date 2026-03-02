project = "mdit-py-plugins"
copyright = "2020, Executable Book Project"
author = "Executable Book Project"

master_doc = "index"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.8", None),
    "markdown_it": ("https://markdown-it-py.readthedocs.io/en/latest", None),
}

html_title = "mdit-py-plugins"
html_theme = "sphinx_book_theme"
html_theme_options = {
    "use_edit_page_button": True,
    "repository_url": "https://github.com/executablebooks/mdit-py-plugins",
    "repository_branch": "master",
    "path_to_docs": "docs",
}
