project = "R3XA_SPEC"
author = "R3XA contributors"
release = "2024.7.1"

extensions = [
    "myst_parser",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"

latex_engine = "pdflatex"
latex_elements = {
    "fontpkg": r"""
\usepackage{tgtermes}
\renewcommand{\sfdefault}{\rmdefault}
""",
}
