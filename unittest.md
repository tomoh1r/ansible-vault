# how to test

1. Create virtualenv.

```console
$ python3 -m venv --clear venv
```

2. Update dependencies.

```console
$ ./venv/bin/python3 -m pip install -U setuptools pip
$ ./venv/bin/python3 -m pip install -e '.[dev]'
```

3. Run test.

```console
$ ./venv/bin/python3 -m pytest
```
