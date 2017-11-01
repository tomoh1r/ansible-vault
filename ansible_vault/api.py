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
from __future__ import absolute_import

import ansible
import yaml
import six
try:
    from ansible.parsing.vault import VaultLib
except ImportError:
    # Ansible<2.0
    from ansible.utils.vault import VaultLib


_ansible_ver = float('.'.join(ansible.__version__.split('.')[:2]))


class Vault(object):
    '''R/W an ansible-vault yaml file'''

    def __init__(self, password):
        self._ansible_ver = _ansible_ver

        self.secret = password.encode('utf-8')
        self.vault = VaultLib(self._make_secrets(self.secret))

    def _make_secrets(self, secret):
        if self._ansible_ver < 2.4:
            return secret

        from ansible.constants import DEFAULT_VAULT_ID_MATCH
        from ansible.parsing.vault import VaultSecret
        return [(DEFAULT_VAULT_ID_MATCH, VaultSecret(secret))]

    def load(self, stream):
        '''read vault steam and return python object'''
        return yaml.safe_load(self.vault.decrypt(stream))

    def dump(self, data, stream=None):
        '''encrypt data and print stdout or write to stream'''
        yaml_text = yaml.dump(
            data,
            default_flow_style=False,
            allow_unicode=True)
        encrypted = self.vault.encrypt(yaml_text)
        if six.PY3: # Handle Python3 Bytestring
            encrypted = encrypted.decode('utf-8')
        if stream:
            stream.write(encrypted)
        else:
            return encrypted
