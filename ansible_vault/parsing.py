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
from abc import ABCMeta, abstractmethod


class VaultLibABC(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def encrypt(self, plaintext):
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, vaulttext):
        raise NotImplementedError


class AnsibleVaultLib(VaultLibABC):
    """Default encrypt/decrypt lib."""

    def __init__(self, secret):
        from ansible.parsing import vault

        self.vault = vault.VaultLib(make_secrets(secret))

    def encrypt(self, plaintext):
        return self.vault.encrypt(plaintext)

    def decrypt(self, vaulttext):
        return self.vault.decrypt(vaulttext)


def make_secrets(secret):
    """Create ansible compatible secret."""
    from ansible.constants import DEFAULT_VAULT_ID_MATCH
    from ansible.parsing import vault

    return [(DEFAULT_VAULT_ID_MATCH, vault.VaultSecret(secret))]
