# Installation

## Setup

Create virtualenv and install packages

```console
$ python3 -m venv --clear .venv
$ .venv/bin/python -m pip install -U setuptools pip wheel
$ .venv/bin/python -m pip install -e '.[dev]'
```

## Dev

Format code

```console
$ .venv/bin/python -m black .
$ .venv/bin/python -m isort .
```

Run test

```console
$ .venv/bin/python -m pytest
```

## Managing repo

Update GitHub wiki

```console
# FIXME: use subtree
```

Install release dep packages, build, and release

```console
$ .venv/bin/python -m pip install -e '.[release]'
$ .venv/bin/python bin/cleanup_build.py
$ .venv/bin/python -m build
$ .venv/bin/python -m twine check dist/*
$ .venv/bin/python -m twine upload --repository testpypi dist/*
$ .venv/bin/python -m twine upload dist/*
```
