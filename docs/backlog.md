# Backlog

## Iteration +1
- Inventory: Access remote `conf.py` at GitHub or HTTP
- Inventory: Unlock `omit_documents` option
- Inventory+Anansi: Add output flavor, like `--details=compact,full`.
  **Full details**, well, should display **full URLs**, ready for
  navigational consumption (clicking).
- Community: Look into intersphinx-untangled.
- Inventory: More attractive JSON output.
  https://github.com/tech-writing/linksmith/pull/4#discussion_r1546863551

## Iteration +2
- MEP 0002 concerns.
- Improve HTML output. (sticky breadcrumb/navbar, etc.)
- Response caching to buffer subsequent invocations
- Anansi: Accept `with_index` and `with_score` options? 
- Anansi: Support project versions by using an ingress notation like
  `flask@2.2`
- Anansi: Expand list of curated projects to essentially any project, with
  support of PyPI, RTD, or other project conventions.
- Speed up `anansi suggest`, maybe introduce `anansi search` instead?

## Done
- Anansi: Display list of curated inventories.
- Anansi: Accept and delegate `threshold` parameter.
- Process multiple objects.inv: Strictness
- Inventory: Unlock accessing intersphinx mappings in `conf.py`
