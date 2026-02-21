from __future__ import annotations

import subprocess
import sys
from pathlib import Path

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
html_static_path = ["_static"]
html_css_files = ["custom.css"]

latex_engine = "pdflatex"
latex_elements = {
    "fontpkg": r"""
\usepackage{tgtermes}
\renewcommand{\sfdefault}{\rmdefault}
""",
}


def _regenerate_spec_artifacts() -> None:
    root = Path(__file__).resolve().parents[1]
    commands = [
        [
            sys.executable,
            str(root / "tools" / "strip_schema.py"),
            str(root / "schema-full.json"),
            str(root / "schema.json"),
        ],
        [
            sys.executable,
            str(root / "tools" / "generate_spec.py"),
            str(root / "schema-full.json"),
            str(root / "docs" / "specification.md"),
        ],
    ]
    for command in commands:
        subprocess.run(command, check=True, cwd=root)


_regenerate_spec_artifacts()
