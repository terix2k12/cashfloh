# Cash-Floh App

A processing tool for accounting data of german finance institutions.
Automatically transforms PDF into structured data based on a configurable rule set.

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

## Bugs
- csv writer robust against semicolon in description

## Backlog
- fix issues in TODO comments
- remove commentend codeparts
- use regex in describe action
- verify hotkeys of categories
- verify categories
- proper description in csv -> add a rule type for it
- remove empty strings fromjson.txt list, vobatransofrmer
- add commit hash in json export
- check condition in debitor?
- multiple actions in one rule
- multiple conditions for one rule
- dont rewrite if already present (except force flag)
- locale in writer
- handle files and folders
- interactive rule creation
- parsing rules configurable
- auto typing linting
- improve rules (and/or)
- add project logo/image

## Issues
- [#1] implement "real" machine learning
- [#2] GUI
- [#3] unittests
- [#4] logging into file (settings)