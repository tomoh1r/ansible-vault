# Samples

## Around VaultLib.

### Use ANSIBLE\_VAULT\_PASSWORD\_FILE.

See [test\_password.py](https://github.com/tomoh1r/ansible-vault/blob/master/test/sample_vault/test_password.py).

```python
from pathlib import Path
from ansible_vault import Vault, VaultLibABC, make_secrets

class MyVaultLib(VaultLibABC):
    def __init__(self):
        fpath = os.environ.get("ANSIBLE_VAULT_PASSWORD_FILE")
        password = open(fpath).read().strip().encode("utf-8")
        self.vlib = VaultLib(make_secrets(password))

    def encrypt(self, plaintext):
        return self.vlib.encrypt(plaintext)

    def decrypt(self, vaulttext):
        return self.vlib.decrypt(vaulttext)


fpath = Path("path") / "to" / "vaulttext.txt"
Vault(vault_lib=MyVaultLib()).load(open(fpath).read())
```

## Around file types.

### PlainText

See [test\_plain.py](https://github.com/tomoh1r/ansible-vault/blob/master/test/sample_io/test_plain.py).

Read from the encrypted file.
```python
from pathlib import Path
from ansible_vault import Vault

fpath = Path("path") / "to" / "vaulttext.txt"
plaintext = Vault("password").load_raw(open(fpath).read())
```

Write to the file.
```python
from pathlib import Path
from ansible_vault import Vault

input_str = "hello, world"

fpath = Path("path") / "to" / "vaulttext.txt"
with open(fpath, "w") as fp:
    Vault("password").dump_raw(input_str.encode("utf-8"), fp)
```

### JSON

See [test\_json.py](https://github.com/tomoh1r/ansible-vault/blob/master/test/sample_io/test_json.py).

Read from the encrypted JSON file.
```python
import json
from pathlib import Path
from ansible_vault import Vault

fpath = Path("path") / "to" / "vaulttext.txt"
json_data = json.loads(Vault("password").load_raw(open(fpath).read()))
```

Write JSON data to the file.
```python
import json
from pathlib import Path
from ansible_vault import Vault

json_data = {"foo": "bar"}

fpath = Path("path") / "to" / "vaulttext.txt"
with open(fpath, "w") as fp:
    Vault("password").dump_raw(json.dumps(json_data).encode("utf-8"), fp)
```
