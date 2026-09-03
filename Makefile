PYTHON ?= python3

.PHONY: all diagrams test validate linkage receipt clean

all: diagrams test validate

diagrams:
	$(PYTHON) scripts/render_architecture.py

test:
	$(PYTHON) -m unittest discover -s tests -v

validate:
	$(PYTHON) scripts/validate_repository.py .

linkage:
	$(PYTHON) scripts/verify_linkage.py --live

receipt:
	mkdir -p artifacts
	$(PYTHON) scripts/create_receipt.py --artifact examples/release/artifact.txt --sbom examples/release/sbom.cdx.json --output artifacts/release-receipt.json

clean:
	rm -rf artifacts site __pycache__ scripts/__pycache__ tests/__pycache__
