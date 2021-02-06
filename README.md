# ansible-vault

[![Test result badge.](https://github.com/tomoh1r/ansible-vault/workflows/test/badge.svg)](https://github.com/tomoh1r/ansible-vault/actions?query=workflow%3Atest) [![Use black.](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

This project aim to R/W an ansible-vault yaml file.

**This is not Ansible official project.**

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

And see [wiki](https://github.com/tomoh1r/ansible-vault/wiki).
