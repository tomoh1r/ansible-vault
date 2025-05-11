#
# Copyright (C) 2017, Tomohiro NAKAMURA <quickness.net@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import os
import shlex
import subprocess
import sys
import tempfile

_PY2 = sys.version_info[0] <= 2


class AnsibleVaultExecutor(object):
    def get_version(self):
        import ansible

        return float(".".join(ansible.__version__.split(".")[:2]))

    def get_executor(self):
        return os.path.join(os.path.dirname(sys.executable), "ansible-vault")

    def encrypt(self, pass_path, plain_fpath):
        pass_opt = "vault-password-file"
        if self.get_version() >= 2.4:
            pass_opt = "vault-id"

        args = f"encrypt --{pass_opt}={pass_path} {plain_fpath}"
        subprocess.check_output(shlex.split(" ".join([self.get_executor(), args])))

    def decrypt(self, pass_path, vault_fpath):
        pass_opt = "vault-password-file"
        if self.get_version() >= 2.4:
            pass_opt = "vault-id"

        args = f"decrypt --{pass_opt}={pass_path} {vault_fpath}"
        subprocess.check_output(shlex.split(" ".join([self.get_executor(), args])))


def encrypt_text(plaintext, encrypt_key, vault_id=None):
    _, plain_fpath = tempfile.mkstemp()
    with open(plain_fpath, "w", encoding="utf-8") as fp:
        fp.write(plaintext)

    _, pass_path = tempfile.mkstemp()
    with open(pass_path, "w", encoding="utf-8") as fp:
        fp.write(encrypt_key)

    try:
        AnsibleVaultExecutor().encrypt(pass_path, plain_fpath)

        with open(plain_fpath, "r", encoding="utf-8") as fp:
            return fp.read()

    finally:
        os.remove(pass_path)
        os.remove(plain_fpath)


def decrypt_text(vaulttext, decrypt_key):
    _, vault_fpath = tempfile.mkstemp()
    with open(vault_fpath, "w", encoding="utf-8") as fp:
        if _PY2 and isinstance(vaulttext, str):
            vaulttext = vaulttext.decode("utf-8")
        elif not _PY2 and isinstance(vaulttext, bytes):
            vaulttext = vaulttext.decode("utf-8")
        fp.write(vaulttext)

    _, pass_path = tempfile.mkstemp()
    with open(pass_path, "w", encoding="utf-8") as fp:
        fp.write(decrypt_key)

    try:
        AnsibleVaultExecutor().decrypt(pass_path, vault_fpath)

        with open(vault_fpath, "r", encoding="utf-8") as fp:
            return fp.read()

    finally:
        os.remove(pass_path)
        os.remove(vault_fpath)
