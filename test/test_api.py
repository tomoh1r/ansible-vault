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

import sys

import pytest
from pkg_resources import parse_version
from yaml.constructor import ConstructorError

_PY2 = sys.version_info[0] <= 2


class _TestBase(object):
    def _getTargetClass(self):
        from ansible_vault import Vault

        return Vault

    def _makeOne(self, password):
        return self._getTargetClass()(password)

    @pytest.fixture()
    def decrypt_text(self, testing):
        return testing.decrypt_text


class TestVaultLoadRaw(_TestBase):
    def test_it(self, vaulted_fp):
        expected = "test\n...\n"
        if not _PY2:
            expected = expected.encode("utf-8")
        assert self._makeOne("password").load_raw(vaulted_fp.read()) == expected


class TestVaultDumpRaw(_TestBase):
    def test_dump_file(self, tmpdir, decrypt_text):
        plaintext = "test"
        secret = "password"

        fp = tmpdir.join("vault.txt")
        self._makeOne(secret).dump_raw(plaintext, fp)

        assert decrypt_text(fp.read(), secret) == plaintext

    def test_dump_text(self, decrypt_text):
        plaintext = "test"
        secret = "password"

        dumped = self._makeOne(secret).dump_raw(plaintext)

        assert decrypt_text(dumped, secret) == plaintext


class TestVaultLoad(_TestBase):
    def test_it(self, vaulted_fp):
        expected = "test"
        assert self._makeOne("password").load(vaulted_fp.read()) == expected


class TestVaultDump(_TestBase):
    def test_dump_file(self, tmpdir, decrypt_text):
        plaintext = "test"
        secret = "password"
        if _PY2:
            plaintext = plaintext.encode("utf-8")

        fp = tmpdir.join("vault.txt")
        self._makeOne(secret).dump(plaintext, fp)

        expected = "test\n...\n"
        assert decrypt_text(fp.read(), secret) == expected

    def test_dump_text(self, decrypt_text):
        plaintext = "test"
        secret = "password"
        if _PY2:
            plaintext = plaintext.encode("utf-8")

        dumped = self._makeOne(secret).dump(plaintext)

        expected = "test\n...\n"
        assert decrypt_text(dumped, secret) == expected


class TestCannotLoadWithInvalidPassword(_TestBase):
    @pytest.mark.parametrize("method_name", ["load_raw", "load"])
    def test_it(self, ansible_ver, vaulted_fp, method_name):
        if ansible_ver < parse_version("2.4"):
            from ansible.errors import AnsibleError as cls

            msg = "Decryption failed"
        else:
            from ansible.parsing.vault import AnsibleVaultError as cls

            msg = "Decryption failed (no vault secrets were found that could decrypt)"

        inst = self._makeOne("invalid-password")
        with pytest.raises(cls) as exc:
            getattr(inst, method_name)(vaulted_fp.read())
        assert str(exc.value) == msg


class TestLoadIsNotpwned(_TestBase):
    def test_it(self, pwned_fp):
        with pytest.raises(ConstructorError):
            self._makeOne("password").load(pwned_fp.read())
