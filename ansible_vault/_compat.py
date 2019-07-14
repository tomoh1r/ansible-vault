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

try:
    from ansible.parsing.vault import VaultLib  # noqa
except ImportError:
    # Ansible<2.0
    from ansible.utils.vault import VaultLib  # noqa


_PY2 = sys.version_info[0] <= 2


def decode_text(text):
    if _PY2 and isinstance(text, str):
        return text.decode("utf-8")
    elif not _PY2 and isinstance(text, bytes):
        return text.decode("utf-8")
    return text
