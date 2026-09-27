# Contributing Guide

## Development

To get started:

```sh
uv venv --python 3.13
uv pip install -e ".[dev]"
pre-commit install
```

Run the checks:

```sh
ruff format qt_themes examples tests
ruff check --select I --fix qt_themes examples tests
ruff check qt_themes examples tests
ty check
pytest
```

### Releasing Changes

To version up using [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release):

```sh
semantic-release version
```
