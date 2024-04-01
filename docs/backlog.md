# Backlog

## Iteration +1
- Docs: Based on sphobjinv.
- Response caching to buffer subsequent invocations
- Add output flavor, like `--details=compact,full`.
  **Full details**, well, should display **full URLs**, ready for
  navigational consumption (clicking).
- Improve HTML output. (sticky breadcrumb/navbar, etc.)

## Iteration +2
sphobjinv call delegation ftw.
```
# Shorthand command ...
anansi suggest matplotlib draw

# ... for:
sphobjinv suggest -u https://matplotlib.org/stable/ draw
```
