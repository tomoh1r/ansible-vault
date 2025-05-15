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
from __future__ import absolute_import, unicode_literals

from importlib import import_module

import pytest
from yaml.constructor import ConstructorError


class TestVaultLoadRaw(object):
    def test_it(self, Vault, vaulted_fp):
        expected = "test\n...\n".encode("utf-8")
        assert Vault("password").load_raw(vaulted_fp.read()) == expected


class TestVaultDumpRaw(object):
    def test_dump_file(self, tmpdir, Vault, decrypt_text):
        plaintext = "test"
        secret = "password"

        fp = tmpdir.join("vault.txt")
        Vault(secret).dump_raw(plaintext, fp)

        assert decrypt_text(fp.read(), secret) == plaintext

    def test_dump_text(self, Vault, decrypt_text):
        plaintext = "test"
        secret = "password"

        dumped = Vault(secret).dump_raw(plaintext)

        assert decrypt_text(dumped, secret) == plaintext


class TestVaultLoad(object):
    def test_it(self, Vault, vaulted_fp):
        expected = "test"
        assert Vault("password").load(vaulted_fp.read()) == expected


class TestVaultDump(object):
    def test_dump_file(self, tmpdir, Vault, decrypt_text):
        plaintext = "test"
        secret = "password"

        fp = tmpdir.join("vault.txt")
        Vault(secret).dump(plaintext, fp)

        expected = "test\n...\n"
        assert decrypt_text(fp.read(), secret) == expected

    def test_dump_text(self, Vault, decrypt_text):
        plaintext = "test"
        secret = "password"

        dumped = Vault(secret).dump(plaintext)

        expected = "test\n...\n"
        assert decrypt_text(dumped, secret) == expected

    def test_dump_additional_parameters(self, Vault, decrypt_text):
        plaintext = "test"
        secret = "password"

        default_style_dumped = Vault(secret).dump(plaintext, default_style='"')
        assert decrypt_text(default_style_dumped, secret) == f'"{plaintext}"\n'

        explicit_start_dumped = Vault(secret).dump(plaintext, explicit_start=True)
        assert decrypt_text(explicit_start_dumped, secret) == f"--- {plaintext}\n...\n"

        canonical_dumped = Vault(secret).dump(plaintext, canonical=True)
        assert decrypt_text(canonical_dumped, secret) == f'---\n!!str "{plaintext}"\n'


class TestCannotLoadWithInvalidPassword(object):
    @pytest.mark.parametrize("method_name", ["load_raw", "load"])
    def test_it(self, Vault, vaulted_fp, method_name):
        cls = import_module("ansible.parsing.vault").AnsibleVaultError
        msg = "Decryption failed (no vault secrets were found that could decrypt)"

        inst = Vault("invalid-password")
        with pytest.raises(cls) as exc:
            getattr(inst, method_name)(vaulted_fp.read())
        assert str(exc.value) == msg


class TestLoadIsNotpwned(object):
    def test_it(self, Vault, pwned_fp):
        with pytest.raises(ConstructorError):
            Vault("password").load(pwned_fp.read())
