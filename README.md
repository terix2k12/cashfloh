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
source cashfloh_venv/bin/activate
pip install uv
uv python list
uv init
uv run -m main
uv add pypdf
uv pip install pypdf
```

### Dependencies

```sh
uv sync --upgrade
```

### Unit- and Regressiontesting

Cashfloh uses pytest. Run tests with:

```sh
uv run pytest
```

### Formatting and Linting

```sh
uv run black .
uv run flake8 cashfloh
```

# TODOS
- proper description in csv
- verify hotkeys of categories
- remove empty strings fromjson.txt list, vobatransofrmer
- check condition in debitor?
- multiple actions in one rule
- multiple conditions for one rule
- dont rewrite if already present (except force flag)
- verify rules
- verify categories
- locale in writer
- handle files and folders
- interactive rule creation
- parsing rules configurable
- auto typing linting
- improve rules
- add project logo/image
- [#1] implement "real" machine learning
- [#2] GUI
- [#3] unittests
- [#4] logging into file (settings)