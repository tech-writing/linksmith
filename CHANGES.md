# Change Log

## Unreleased

## v0.0.0 - 2024-xx-xx
- Implement `linksmith inventory` and `linksmith output-formats`
  subcommands, based on `sphobjinv` and others. Thanks, @bskinn.
- Anansi: Implement `linksmith anansi suggest`, also available as `anansi`,
  to easily suggest terms of a few curated community projects.
  Thanks, @bskinn.
- Accept `linksmith inventory` without `INFILES` argument, implementing
  auto-discovery of `objects.inv` in local current working directory.
- Anansi: Manage project list in YAML file `curated.yaml`, not Python.
- Anansi: Provide `anansi list-projects` subcommand, to list curated
  projects managed in accompanying `curated.yaml` file.
