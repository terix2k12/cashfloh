# Cash-Floh App

A processing tool for accounting data of german finance institutions.

## Execution

```sh
python3 -m cashfloh --profile default /path/to/input/files/
```

## Development

### Setup

Create a local virtual environment (venv), then install `uv`.

For example for Python 3.12 under Ubuntu/Debian:
```sh
python3 -m venv cashfloh_venv
cashfloh_venv/bin/pip install uv
cashfloh_venv/bin/uv python list
cashfloh_venv/bin/uv init
cashfloh_venv/bin/uv run -m main
cashfloh_venv/bin/uv add pypdf
cashfloh_venv/bin/uv pip install pypdf
```

### Unit- and Regressiontests

Cashfloh uses pytest. Run tests with:

```sh
cashfloh_venv/bin/uv run pytest
```

### Formatting and Linting

```sh
cashfloh_venv/bin/uv run black .
cashfloh_venv/bin/uv run flake8 cashfloh
```

# TODOS
- mulitple actions in one rule
- dont rewrite if already present (except force flag)
- verify rules
- verify categories
- locale in writer
- handle files and folders
- remove wild venv from readme
- interactive rule creation
- logging into file (settings)
- parsing rules configurable
- auto typing linting
- unittests
- improve rules
- implement "real" machine learning
- GUI
