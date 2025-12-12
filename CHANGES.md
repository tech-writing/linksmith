# Change Log

## Unreleased
- Anansi: Fixed RTD project discovery

## v0.0.1 - 2024-04-06
- Inventory: Implement `linksmith inventory` and `linksmith output-formats`
  subcommands, based on `sphobjinv` and others. Thanks, @bskinn.
- Anansi: Implement `linksmith anansi suggest`, also available as `anansi`,
  to easily suggest terms of a few curated community projects.
  Thanks, @bskinn.
- Inventory: Accept `linksmith inventory` without `INFILES` argument,
  implementing auto-discovery of `objects.inv` in local current working
  directory.
- Anansi: Manage project list in YAML file `curated.yaml`, not Python.
- Anansi: Provide `anansi list-projects` subcommand, to list curated
  projects managed in accompanying `curated.yaml` file.
- Anansi: Accept `--threshold` option, forwarding to `sphobjinv`.
- Anansi: Discover `objects.inv` also from RTD and PyPI.
- Inventory: Implement auto-discovery of `conf.py`, including traversal
  of `intersphinx_mapping`. Thanks, @chrisjsewell.
