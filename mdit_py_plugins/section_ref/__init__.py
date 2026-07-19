"""Section reference plugin for markdown-it-py.

Captures section-sign references such as ``§1``, ``§1.1`` and ``§2.3.4``
into dedicated ``section_ref`` tokens, so downstream renderers
(e.g. MyST-Parser) can resolve them to numbered heading cross-references.

Requires markdown-it-py >= 4.1.0.
"""

from .index import section_ref_plugin

__all__ = ("section_ref_plugin",)
