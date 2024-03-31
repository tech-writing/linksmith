# Linksmith

_A program for processing Hyperlinks, Sphinx references, and inventories._

Longing for a Hyperlink, \
already in hand. \
MEP 0002, \
considering.

» [Documentation]
| [Changelog]
| [PyPI]
| [Issues]
| [Source code]
| [License]

[![CI][badge-tests]][project-tests]
[![Coverage status][badge-coverage]][project-codecov]


## Why

- Grown out of passion for [Sphinx], [Hyperlinks], and [DWIM],
  and a sweet conversation at pueblo's sketch about [adding an inventory
  decoder for Sphinx].
- To learn [sphobjinv], and explore a few convenience heuristics around it.
- To host code for community operations, alongside software tests and
  packaging, in order to provide better maintainability and code re-use.
- Along the lines of shuffling code around, provide a few tangible features
  [collected the other day][rfc].


## Setup

```bash
pip install 'linksmith @ git+https://github.com/tech-writing/linksmith.git'
```


## Usage
Nothing works yet. All just sketched out.

sphobjinv call delegation ftw.
```
# Shorthand command ...
anansi suggest matplotlib draw

# ... for:
sphobjinv suggest -u https://matplotlib.org/stable/ draw
```



## Development

In order to learn how to set up a development sandbox, please visit the
[development documentation].


## Contributing

We are always happy to receive code contributions, ideas, suggestions
and problem reports from the community.

Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue ticket.

Thanks in advance for your efforts, we really appreciate any help or feedback.


## Etymology

> Anansi, or Ananse (/əˈnɑːnsi/ ə-NAHN-see) is an Akan folktale character
> associated with stories, wisdom, knowledge, and trickery.
>
> Anansi is best known for his ability to outsmart and triumph over more
> powerful opponents through his use of cunning, creativity and wit.
>
> Despite taking on a trickster role, Anansi often takes centre stage in
> stories and is commonly portrayed as both the protagonist and antagonist. 
>
> -- https://en.wikipedia.org/wiki/Anansi

Another [`anansi`] package has already been published to PyPI, so we needed
to find a different name, and selected [`linksmith`] for the time being.
_If you have other suggestions as long as this program is in its infancy,
please let us know._


## Acknowledgements

Kudos to [Sviatoslav Sydorenko], [Brian Skinn], [Chris Sewell], and all other
lovely people around Sphinx and Read the Docs.


[adding an inventory decoder for Sphinx]: https://github.com/pyveci/pueblo/pull/73
[`anansi`]: https://pypi.org/project/anansi/
[Brian Skinn]: https://github.com/bskinn
[Chris Sewell]: https://github.com/chrisjsewell
[development documentation]: https://linksmith.readthedocs.io/en/latest/sandbox.html
[DWIM]: https://en.wikipedia.org/wiki/DWIM
[Hyperlink]: https://en.wikipedia.org/wiki/Hyperlink
[Hyperlinks]: https://en.wikipedia.org/wiki/Hyperlink
[linksmith]: https://linksmith.readthedocs.io/
[`linksmith`]: https://pypi.org/project/linksmith/
[rfc]: https://linksmith.readthedocs.io/en/latest/rfc.html
[Sphinx]: https://www.sphinx-doc.org/
[sphobjinv]: https://sphobjinv.readthedocs.io/
[Sviatoslav Sydorenko]: https://github.com/webknjaz

[Changelog]: https://github.com/tech-writing/linksmith/blob/main/CHANGES.md
[Documentation]: https://linksmith.readthedocs.io/
[Issues]: https://github.com/tech-writing/linksmith/issues
[License]: https://github.com/tech-writing/linksmith/blob/main/LICENSE
[PyPI]: https://pypi.org/project/linksmith/
[Source code]: https://github.com/tech-writing/linksmith

[badge-coverage]: https://codecov.io/gh/tech-writing/linksmith/branch/main/graph/badge.svg
[badge-downloads-per-month]: https://pepy.tech/badge/linksmith/month
[badge-license]: https://img.shields.io/github/license/tech-writing/linksmith.svg
[badge-package-version]: https://img.shields.io/pypi/v/linksmith.svg
[badge-python-versions]: https://img.shields.io/pypi/pyversions/linksmith.svg
[badge-status]: https://img.shields.io/pypi/status/linksmith.svg
[badge-tests]: https://github.com/tech-writing/linksmith/actions/workflows/main.yml/badge.svg
[project-codecov]: https://codecov.io/gh/tech-writing/linksmith
[project-downloads]: https://pepy.tech/project/linksmith/
[project-license]: https://github.com/tech-writing/linksmith/blob/main/LICENSE
[project-pypi]: https://pypi.org/project/linksmith
[project-tests]: https://github.com/tech-writing/linksmith/actions/workflows/main.yml
