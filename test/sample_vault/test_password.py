#
# Copyright (C) 2021, Tomohiro NAKAMURA <quickness.net@gmail.com>
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
# pylint: disable=R0917
from __future__ import absolute_import, unicode_literals

import os
from importlib import import_module

import pytest


class TestVault(object):
    _vault_key = "password"

    @pytest.fixture()
    def MyVaultLib(self, VaultLib):
        make_secrets = import_module("ansible_vault").make_secrets

        class Cls(import_module("ansible_vault").VaultLibABC):
            def __init__(self):
                fpath = os.environ.get("ANSIBLE_VAULT_PASSWORD_FILE")
                with open(fpath, "r", encoding="utf-8") as fp:
                    password = fp.read().strip().encode("utf-8")
                self.vlib = VaultLib(make_secrets(password))

            def encrypt(self, plaintext):
                return self.vlib.encrypt(plaintext)

            def decrypt(self, vaulttext):
                return self.vlib.decrypt(vaulttext)

        return Cls

    @pytest.fixture()
    def password_file(self, tmp_path):
        fpath = str(tmp_path / "passwd.txt")
        with open(fpath, "w", encoding="utf-8") as fp:
            fp.write(self._vault_key + "\n")
        return fpath

    def test_load(self, monkeypatch, Vault, MyVaultLib, password_file, vaulted_fp):
        monkeypatch.setenv("ANSIBLE_VAULT_PASSWORD_FILE", password_file)

        inst = Vault(vault_lib=MyVaultLib())
        assert inst.load(vaulted_fp.read()) == "test"

    def test_dump_text(self, monkeypatch, Vault, decrypt_text, MyVaultLib, password_file):
        monkeypatch.setenv("ANSIBLE_VAULT_PASSWORD_FILE", password_file)

        inst = Vault(vault_lib=MyVaultLib())
        dumped = inst.dump_raw("test")
        assert decrypt_text(dumped, self._vault_key) == "test"
