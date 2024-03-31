---
title: |
  Requests for Comments around Linksmith, a program for processing Hyperlinks,
  Sphinx references, and inventories.
document:
  id: 'linksmith-rfc'
  created: '2024-03-31'
  authors:
    - Andreas Motl @amotl
    - Brian Skinn @bskinn
    - Sviatoslav Sydorenko @webknjaz
  status: Draft
---

(rfc)=

# Linksmith RFC

This document originates from an excellent conversation at pueblo's sketch
about [adding an inventory decoder for Sphinx].

It is an informal living document, and may be enhanced through gists from
other and subsequent conversations as we go.
Contributions of any kind are very much appreciated and welcome.


(rfc-objectives)=
## Objectives

Exploring a few ideas around the topics shared below, in order to create
an optimal linksmith program, mostly just a gobble of glue code, calling out
to existing tools and libraries, and poly-filling the gaps.

- `sphobjinv` doesn't know how to introspect `conf.py:intersphinx_mapping`,
  to go from project name to docset URL.
- `sphobjinv` is meant to be able to run whether or not the user is in a
  Sphinx documentation directory tree.
- People are asking for [](#rfc-markdown-output), but `sphobjinv` will unlikely
  implement it.
- People are asking for [](#rfc-multi-project), but `sphobjinv` doesn't
  have it.
- Colleagues are running [](#rfc-community-operations) like Sviatoslav's
  [intersphinx-untangled], or Brian's [intersphinx-gist], with code that
  is not packaged for reusability.
- MyST support, specifically [](inv:mep#meps/mep-0002), should not be left
  behind, but instead should be considered from the very beginning. _Primarily_
  using Markdown will certainly be the future of technical writing with Sphinx.
- Focus on technically relevant details around Sphinx references, cross-
  references, and inventories, but also don't forget about style, using the
  new [Hyper] role, and friends.


(rfc-markdown-output)=
### Markdown Output

>> Maybe Markdown output has not been considered yet?
>
> Markdown **_output_**? Why?

We usually reach out to Markdown generation these days, because the output can
be used both as a text-only variant, and for upgrading to HTML by sending it
through a corresponding Markdown renderer.

In this way, text output from utility programs becomes super versatile, because
it can be easily shared on all systems understanding Markdown, like
[Sphinx]/[MyST], GitHub, Discourse, or even Grafana, all tools we use most of
the time for information sharing and conveyance.

By using Markdown, it was easy to convey different sections of output into a
single output file. In this case, the inventory decoder needed to take into
account that we wanted to include intersphinx references for **multiple
projects**, effectively all inventory files listed in [sphinx-inventories.txt].

This has now converged into https://github.com/crate/crate-docs/issues/105, not
quite reaching the goal yet, because the generated Markdown became too large to
be shared on behalf of a GitHub comment 🙈.


(rfc-multi-project)=
### Multi-Project Support

Provide different means of seeding / wrapping around `sphobjinv` using
multiple projects.

>> It would be straightforward to write a wrapper [to handle multi-project]
>> processing. [...] [However,] I don't consider it within `sphobjinv`'s
>> purview to actually _be_ that consolidating wrapper, though. 
>
> We will be happy to explore this on behalf of `linksmith`, by
> pulling in `sphobjinv`. Excellent! Because we have the need for standalone
> usage (i.e. without access to `conf.py`), we consider this wrapper to receive
> the following features aka. **variants**, to seed a list of projects:

- Parse `intersphinx_mapping` out of `conf.py`, like suggested by @chrisjsewell.
- Use a list of paths or URLs to multiple `objects.inv` files, like 
  [sphinx-inventories.txt], either by providing a file, or on stdin/cmdline.
  This reflects the use case we have, based on the code in [tasks.py].
- Autodiscovery-like features on top of both variants: For example, a `conf.py`
  can be local or on a remote URL, possibly within a `doc` or `docs` folder
  within a Git project pointed at. Similarly, an `objects.inv` file can be
  located within a `{doc,docs}/_build/` folder within a typical Git project,
  or within a `/en/latest` URL path when hosted on RTD, for example. That
  would be just a bunch of convenience heuristics on top for people who want them.
- Consider how the [new `references` builder in Sphinx] by @chrisjsewell could be
  used in this context.


(rfc-community-operations)=
### Community Operations

- Consider the use case of @webknjaz, to run a multi-tenant static intersphinx
  generator operation, on behalf of a list of projects like [sphinx-websites.yml],
  based on [relevant code to generate a static website], if he doesn't have any
  objections about it?

- In order to further increase community support and leverage, fragments of @bskinn's
  community operations around [intersphinx-gist] and [intersphinx_mappings.txt] could
  also be absorbed into code instead of hosting it on behalf of a text file in a gist.

> My thinking here is that if you already have a tool in hand that takes care about
> those topics in a generalized way, it would feel like an artificial boundary why it
> would only work on _local_ projects.

In the same spirit like @webknjaz curated a list of popular Python projects on behalf
of intersphinx-untangled in YAML format, and @bskinn did on behalf of the
intersphinx_mappings.txt Gist, those lists could also be written down or wrapped through
Python, in order to provide easy command-line access, right?




[adding an inventory decoder for Sphinx]: https://github.com/pyveci/pueblo/pull/73
[Hyperlink]: https://en.wikipedia.org/wiki/Hyperlink
[Hyperlinks]: https://en.wikipedia.org/wiki/Hyperlink
[Hyper]: https://sphinx-design-elements--71.org.readthedocs.build/en/71/hyper.html
[intersphinx-gist]: https://github.com/bskinn/intersphinx-gist
[intersphinx-untangled]: https://github.com/webknjaz/intersphinx-untangled
[intersphinx_mappings.txt]: https://gist.github.com/bskinn/0e164963428d4b51017cebdb6cda5209
[MEP 0002]: https://mep.mystmd.org/en/latest/meps/mep-0002/
[MyST]: https://myst-parser.readthedocs.io/
[new `references` builder in Sphinx]: https://github.com/sphinx-doc/sphinx/pull/12190
[relevant code to generate a static website]: https://github.com/webknjaz/intersphinx-untangled/blob/5d495581ec9e9096aa503c7281089f0a883be619/.github/workflows/build-gh-pages.yml#L29-L82
[Sphinx]: https://www.sphinx-doc.org/
[sphinx-design]: https://sphinx-design.readthedocs.io/
[sphinx-inventories.txt]: https://github.com/crate/crate-docs/blob/main/registry/sphinx-inventories.txt
[sphinx-websites.yml]: https://github.com/webknjaz/intersphinx-untangled/blob/master/sphinx-websites.yml
[sphobjinv]: https://sphobjinv.readthedocs.io/
[tasks.py]: https://github.com/crate/crate-docs/blob/main/tasks.py
