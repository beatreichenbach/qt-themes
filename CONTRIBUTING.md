# Contributing Guide


### Create a virtual environment

Create a venv:
```shell
python -m venv venv
```

Activate it on Linux and macOS:
```shell
source venv/bin/activate
```
Or on Windows:
```shell
.\venv\Scripts\activate.bat
```

### Install the Development Dependencies.

Install `qt-themes` in editable mode:
```shell
python -m pip install -e .[dev]
```

### Releasing Changes

To version up using [python-semantic-release]:
```shell
semantic-release version
```

[python-semantic-release]: https://github.com/python-semantic-release/python-semantic-release
