# ansible-vault

**This is not an official Ansible project.**

This project aim to R/W an ansible-vault yaml file.

[![test](https://github.com/tomoh1r/ansible-vault/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/tomoh1r/ansible-vault/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/tomoh1r/ansible-vault/badge.svg?branch=master)](https://coveralls.io/github/tomoh1r/ansible-vault?branch=master)
[![PyPI - Version](https://img.shields.io/pypi/v/ansible-vault)](https://pypi.org/project/ansible-vault/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ansible-vault)
![ansible-core Support Version](https://img.shields.io/badge/misc-2.16%20%7C%202.17%20%7C%202.18-blue?label=ansible-vault)
![GitHub License](https://img.shields.io/github/license/tomoh1r/ansible-vault)

---

## Quick Start

You can install with pip.

```console
pip install ansible-vault
```

When you have an ansible-vault file, then you can read file. See below.

```python
from ansible_vault import Vault

vault = Vault('password')
data = vault.load(open('vault.yml').read())
```

When you have to write data, then you can write data to file. See below.

```python
from ansible_vault import Vault

vault = Vault('password')
vault.dump(data, open('vault.yml', 'w'))

# also you can get encrypted text
print(vault.dump(data))
```

## Contributing

See [CONTRIBUTING.md](https://github.com/tomoh1r/ansible-vault/blob/master/CONTRIBUTING.md).

---

## Links

* [Repository wiki](https://github.com/tomoh1r/ansible-vault/wiki)
