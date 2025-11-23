# Cash-Floh App

A processing tool for accounting information of german finance institutions.

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
cashfloh_venv/bin/uv run flake8 app
```

# TODOS
- apply for dkb too
- interactive correction 
- Replace Category/Subcategory ENUMS with configurable values
- export to ODS/CSV/TXT
- GUI
- implement "real" machine learning
- parsing rules configurable
- auto typing linting
- unittests