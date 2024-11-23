"""Configuration file for the Sphinx documentation builder."""

import os

project = "Linksmith"
copyright = "2023-2024, Panodata Developers"  # noqa: A001
author = "Panodata Developers"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_design_elements",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

html_theme = os.environ.get("SPHINX_THEME", "furo")
html_title = "Linksmith"
# html_title = f"Linksmith ({html_theme.replace('_', '-')})"

html_static_path = ["_static"]
# html_logo = "_static/logo_wide.svg"
# html_favicon = "_static/logo_square.svg"

# TODO: Is it needed?
html_css_files = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/fontawesome.min.css"]
html_theme_options = {
    "sidebar_hide_name": False,
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
myst_enable_extensions = [
    "attrs_block",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_substitutions = {}

# Configure Sphinx-copybutton
copybutton_remove_prompts = True
copybutton_line_continuation_character = "\\"
copybutton_prompt_text = r">>> |\.\.\. |\$ |sh\$ |PS> |cr> |mysql> |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

# Configure Intersphinx
intersphinx_mapping = {
    "mep": ("https://mep.mystmd.org/", None),
    "myst": ("https://myst-parser.readthedocs.io/en/latest/", None),
    "sd": ("https://sphinx-design.readthedocs.io/en/latest/", None),
    "sde": ("https://sphinx-design-elements.readthedocs.io/en/latest/", None),
    "soi": ("https://sphobjinv.readthedocs.io/en/stable/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

todo_include_todos = True
