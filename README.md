# R3XA_SPEC

Reference repository for the R3XA schema and generated specification documents.

## Repository layout

- `schema-full.json`: source-of-truth schema.
- `schema.json`: runtime-optimized schema generated from `schema-full.json`.
- `tools/strip_schema.py`: strips editorial keys from `schema-full.json`.
- `tools/generate_spec.py`: generates an agnostic `docs/specification.md`.
- `docs/specification.md`: generated specification document.
- `docs/conf.py`: Sphinx configuration for HTML/PDF documentation.

## Quick start

```bash
make all
```

This generates:

- `schema.json`
- `docs/specification.md`

## Check generated artifacts

```bash
make check-generated
```

This runs generation and fails if committed files are out of date.

## Build documentation with Sphinx

Install docs dependencies:

```bash
pip install -e .[docs]
```

Build HTML:

```bash
make html
```

Generate PDF:

```bash
make pdf
```

`make pdf` uses the Sphinx LaTeX builder and requires a local LaTeX toolchain (for example `latexmk` + TeX Live).

## Read the Docs

Read the Docs is configured through `.readthedocs.yaml` and builds from Sphinx (`docs/conf.py`).
PDF export is enabled with RTD `formats: [pdf]`.
The Sphinx config regenerates `schema.json` and `docs/specification.md` automatically at build time.

### Enable online Read the Docs

1. Go to <https://app.readthedocs.org/>.
2. Click **Add project**.
3. Import `jeffwitz/R3XA_SPEC` from GitHub.
4. Confirm the default branch (`main`).
5. Keep config file mode enabled (`.readthedocs.yaml`).
6. Launch the first build.
7. Check:
   - HTML: `/en/latest/`
   - PDF: **Download PDF** button on the project page.

For a local RTD-like check:

```bash
python -m sphinx -T -b html -d docs/_build/doctrees -D language=en docs docs/_build/rtd-html
```

## Contributing

Open an issue to discuss schema changes before editing `schema-full.json`.
Generated files (`schema.json`, `docs/specification.md`) must be updated in the same PR.
