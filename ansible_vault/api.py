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

import json

import ansible
import yaml

from ._compat import VaultLib, decode_text

_ANSIBLE_VER = float(".".join(ansible.__version__.split(".")[:2]))


class Vault(object):
    """R/W an ansible-vault yaml file"""

    class FileTypes:
        JSON = "json"
        YAML = "yaml"

    def __init__(self, password, file_type=FileTypes.JSON):
        self.secret = password.encode("utf-8")
        self.vault = VaultLib(self._make_secrets(self.secret))
        self.file_type = file_type

        if file_type not in [self.FileTypes.JSON, self.FileTypes.YAML]:
            raise Exception("Bad File Type: %s" % self.file_type)

    def _make_secrets(self, secret):
        if _ANSIBLE_VER < 2.4:
            return secret

        from ansible.constants import DEFAULT_VAULT_ID_MATCH
        from ansible.parsing.vault import VaultSecret

        return [(DEFAULT_VAULT_ID_MATCH, VaultSecret(secret))]

    def load_raw(self, stream):
        """Read vault stream and return raw data."""
        return self.vault.decrypt(stream)

    def dump_raw(self, text, stream=None):
        """Encrypt raw data and write to stream."""
        encrypted = decode_text(self.vault.encrypt(text))
        if stream:
            stream.write(encrypted)
        else:
            return encrypted

    def load(self, stream):
        """Read vault steam and return python object."""
        if self.file_type == self.FileTypes.YAML:
            result = yaml.safe_load(self.load_raw(stream))
        else:
            result = json.loads(self.load_raw(stream))

        return result

    def dump(self, data, stream=None):
        """Encrypt data and print stdout or write to stream."""
        yaml_text = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        return self.dump_raw(yaml_text, stream=stream)
