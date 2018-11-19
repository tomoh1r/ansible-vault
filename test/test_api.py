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
import sys

import pytest
from yaml.constructor import ConstructorError

from ansible_vault.testing import decrypt_text


PY3 = sys.version_info[0] > 2


class _TestBase(object):
    def _getTargetClass(self):
        from ansible_vault import Vault
        return Vault

    def _makeOne(self, password):
        return self._getTargetClass()(password)


class TestVaultLoadRaw(_TestBase):
    def test_can(self, vaulted_fp):
        actual = self._makeOne('password').load_raw(vaulted_fp.read())
        expected = 'test\n...\n'
        if PY3:
            expected = expected.encode('utf-8')
        assert actual == expected

    def test_cannot(self, ansible_ver, vaulted_fp):
        if ansible_ver < 2.4:
            from ansible.errors import AnsibleError as cls
            msg = 'Decryption failed'
        else:
            from ansible.parsing.vault import AnsibleVaultError as cls
            msg = ('Decryption failed '
                   '(no vault secrets would found that could decrypt)')

        with pytest.raises(cls, message=msg):
            self._makeOne('invalid-password').load_raw(vaulted_fp.read())


class TestVaultDumpRaw(_TestBase):
    def test_dump_file(self, tmpdir):
        plaintext = 'test'
        secret = 'password'

        fp = tmpdir.join('vault.txt')
        self._makeOne(secret).dump_raw(plaintext, fp)

        assert decrypt_text(fp.read(), secret) == plaintext

    def test_dump_text(self):
        plaintext = 'test'
        secret = 'password'

        dumped = self._makeOne(secret).dump_raw(plaintext)

        assert decrypt_text(dumped, secret) == plaintext


class TestVaultLoad(_TestBase):
    def test_can(self, vaulted_fp):
        assert self._makeOne('password').load(vaulted_fp.read()) == 'test'

    def test_cannot(self, ansible_ver, vaulted_fp):
        if ansible_ver < 2.4:
            from ansible.errors import AnsibleError as cls
            msg = 'Decryption failed'
        else:
            from ansible.parsing.vault import AnsibleVaultError as cls
            msg = ('Decryption failed '
                   '(no vault secrets would found that could decrypt)')

        with pytest.raises(cls, message=msg):
            self._makeOne('invalid-password').load(vaulted_fp.read())

    def test_not_pwned(self, pwned_fp):
        with pytest.raises(ConstructorError):
            self._makeOne('password').load(pwned_fp.read())


class TestVaultDump(_TestBase):
    def test_dump_file(self, tmpdir):
        plaintext = 'test'
        secret = 'password'

        fp = tmpdir.join('vault.txt')
        self._makeOne(secret).dump(plaintext, fp)

        assert decrypt_text(fp.read(), secret) == plaintext + '\n...\n'

    def test_dump_text(self):
        plaintext = 'test'
        secret = 'password'

        dumped = self._makeOne(secret).dump(plaintext)

        assert decrypt_text(dumped, secret) == plaintext + '\n...\n'

    def test_dump_additional_parameters(self):
        plaintext = 'test'
        secret = 'password'

        default_style_dumped = self._makeOne(secret).dump(plaintext, default_style='"')

        assert decrypt_text(default_style_dumped, secret) == f'"{plaintext}"\n'

        explicit_start_dumped = self._makeOne(secret).dump(plaintext, explicit_start=True)

        assert decrypt_text(explicit_start_dumped, secret) == f'--- {plaintext}\n...\n'

        canonical_dumped = self._makeOne(secret).dump(plaintext, canonical=True)

        assert decrypt_text(canonical_dumped, secret) == f'---\n!!str "{plaintext}"\n'
