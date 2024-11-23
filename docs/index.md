# Linksmith

Linksmith is a program for processing Hyperlinks, Sphinx references,
and inventories.

It is heavily based on [`sphinx.ext.intersphinx`] and [sphobjinv], and
intends to provide [DWIM]-like tooling for [Sphinx] references and
[Hyperlinks].

::::::{grid} 1 3 3 3
:margin: 4 4 0 0
:padding: 0
:gutter: 2

::::{grid-item-card} {material-outlined}`lightbulb;1.5em` Haiku
:shadow: md
Longing for a Hyperlink, \
already in hand. \
MEP 0002, \
considering.
::::

::::{grid-item-card} {material-outlined}`menu_book;1.5em` Usage
:shadow: md
:link: usage
:link-type: ref
Guidelines and examples how to use the `linksmith`
and `anansi` command line programs.
::::

::::{grid-item-card} {material-outlined}`group;1.5em` RFC
:shadow: md
:link: rfc
:link-type: ref
Just the proposal, nothing more.

- [](#rfc-markdown-output)
- [](#rfc-multi-project)
- [](#rfc-community-operations)
::::

::::::


:::{toctree}
:caption: Handbook
:hidden:

rfc
setup
usage
:::


:::{toctree}
:caption: Workbench
:hidden:

project
sandbox
backlog
:::


:::{note}
Intrigued by MEP 0002? Enjoy reading [](inv:mep#mep-0002).
:::

:::{tip}
Linksmith is a work-in-progress, and is still in its infancy, appreciating any
contributions to satisfy community needs.
In order to start contributing to Linksmith, please refer to the documentation
page about how to set up a [](#development-sandbox).
:::


[DWIM]: https://en.wikipedia.org/wiki/DWIM
[Hyperlinks]: https://en.wikipedia.org/wiki/Hyperlink
[Sphinx]: https://www.sphinx-doc.org/
[`sphinx.ext.intersphinx`]: https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
[sphobjinv]: https://sphobjinv.readthedocs.io/
