(usage)=
# Usage

Linksmith provides the `linksmith` command line program. It harbours
different subsystems, accessible by using corresponding subcommands,
like `linksmith inventory`.

:::{warning}
Here be dragons. Please note the program is pre-alpha, and a work in
progress, so everything may change while we go.
:::


## Output Formats
Display all the available output formats at a glance.
```shell
linksmith output-formats
```


## Sphinx Inventories
The `linksmith inventory` subsystem supports working with Sphinx inventories,
it is heavily based on `sphinx.ext.intersphinx` and `sphobjinv`. 

:::{rubric} Single Inventory
:::
Refer to `objects.inv` on the local filesystem or on a remote location.
```shell
linksmith inventory /path/to/objects.inv
```
```shell
linksmith inventory https://linksmith.readthedocs.io/en/latest/objects.inv
```

```shell
linksmith inventory \
  https://linksmith.readthedocs.io/en/latest/objects.inv \
  --format=markdown+table
```

:::{rubric} Multiple Inventories
:::
Refer to multiple `objects.inv` resources.
```shell
linksmith inventory \
  https://github.com/crate/crate-docs/raw/main/registry/sphinx-inventories.txt \
  --format=html+table
```


:::{rubric} Auto-Discovery
:::
Discover `objects.inv` in working directory.
```shell
linksmith inventory
```


## Anansi

Suggest references from curated intersphinx inventories.

:::{rubric} Synopsis
:::

```shell
anansi suggest matplotlib draw
```

```shell
anansi suggest sarge capture
```
