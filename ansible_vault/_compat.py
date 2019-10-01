#
# Copyright (C) 2019, Tomohiro NAKAMURA <quickness.net@gmail.com>
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

from ansible_vault._vendored import ansible
from ansible_vault._vendored.ansible.parsing.vault import VaultLib  # noqa

ANSIBLE_VERSION = float(".".join(ansible.__version__.split(".")[:2]))

_PY2 = sys.version_info[0] <= 2


def make_secrets(secret):
    if ANSIBLE_VERSION < 2.4:
        return secret

    from ansible_vault._vendored.ansible.constants import DEFAULT_VAULT_ID_MATCH
    from ansible_vault._vendored.ansible.parsing.vault import VaultSecret

    return [(DEFAULT_VAULT_ID_MATCH, VaultSecret(secret))]


def decode_text(text):
    if _PY2 and isinstance(text, str):
        return text.decode("utf-8")
    elif not _PY2 and isinstance(text, bytes):
        return text.decode("utf-8")
    return text
