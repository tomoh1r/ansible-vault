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
    _plaintext = "test"
    _secret = "password"

    def test_dump_file(self, tmpdir, Vault, testing):
        fp = tmpdir.join("vault.txt")
        Vault(self._secret).dump_raw(self._plaintext, fp)

        assert testing.decrypt_text(fp.read(), self._secret) == self._plaintext

    def test_dump_text(self, Vault, testing):
        dumped = Vault(self._secret).dump_raw(self._plaintext)

        assert testing.decrypt_text(dumped, self._secret) == self._plaintext


class TestVaultLoad(object):
    def test_it(self, Vault, vaulted_fp):
        expected = "test"
        assert Vault("password").load(vaulted_fp.read()) == expected


class TestVaultDump(object):
    _plaintext = "test"
    _secret = "password"

    def test_dump_file(self, tmpdir, Vault, testing):
        fp = tmpdir.join("vault.txt")
        Vault(self._secret).dump(self._plaintext, fp)

        expected = "test\n...\n"
        assert testing.decrypt_text(fp.read(), self._secret) == expected

    def test_dump_text(self, Vault, testing):
        dumped = Vault(self._secret).dump(self._plaintext)

        expected = "test\n...\n"
        assert testing.decrypt_text(dumped, self._secret) == expected

    @pytest.mark.parametrize(
        "kwargs,expected",
        [
            [{"default_style": '"'}, '"test"\n'],
            [{"explicit_start": True}, "--- test\n...\n"],
            [{"canonical": True}, '---\n!!str "test"\n'],
        ],
    )
    def test_dump_additional_parameters(self, Vault, testing, kwargs, expected):
        default_style_dumped = Vault(self._secret).dump(self._plaintext, **kwargs)
        assert testing.decrypt_text(default_style_dumped, self._secret) == expected


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
