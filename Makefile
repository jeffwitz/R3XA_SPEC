.PHONY: all schema generate-schema spec generate-spec html docs pdf check-generated clean

PYTHON ?= python3
SPHINXBUILD ?= $(PYTHON) -m sphinx
SPHINX_DOCS_DIR ?= docs
SPHINX_BUILD_DIR ?= docs/_build

all: schema spec

schema generate-schema:
	$(PYTHON) tools/strip_schema.py schema-full.json schema.json

spec generate-spec: schema
	$(PYTHON) tools/generate_spec.py schema-full.json docs/specification.md

html docs: spec
	$(SPHINXBUILD) -b html $(SPHINX_DOCS_DIR) $(SPHINX_BUILD_DIR)/html

pdf: spec
	$(SPHINXBUILD) -M latexpdf $(SPHINX_DOCS_DIR) $(SPHINX_BUILD_DIR)

check-generated: all
	git diff --exit-code schema.json docs/specification.md

clean:
	rm -f schema.json docs/specification.md
	rm -rf $(SPHINX_BUILD_DIR)
