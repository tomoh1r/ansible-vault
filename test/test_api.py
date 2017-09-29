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
import pytest
from yaml.constructor import ConstructorError

from ansible_vault.testing import decrypt_text


class TestVaultLoad(object):
    def _getTargetClass(self):
        from ansible_vault import Vault
        return Vault

    def _makeOne(self, password):
        return self._getTargetClass()(password)

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


class TestVaultDump(object):
    def _getTargetClass(self):
        from ansible_vault import Vault
        return Vault

    def _makeOne(self, password):
        return self._getTargetClass()(password)

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
