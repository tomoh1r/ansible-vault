# coding: utf-8
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
from __future__ import absolute_import, unicode_literals

import sys

import pytest

_PY2 = sys.version_info[0] <= 2


@pytest.mark.parametrize(
    "input_str,expected", [("test", "test"), ("あいうえお", "あいうえお"), ("test\nあいうえお", "test\nあいうえお")]
)
class TestVaultWithPlainText(object):
    _secret = "password"

    def test_read_from_encrypted_plain_text(
        self, tmp_path, Vault, encrypt_text, input_str, expected
    ):
        if _PY2:
            input_str = input_str.encode("utf-8")
        fpath = str((tmp_path / "vault.txt").absolute())
        with open(fpath, "w") as fp:
            fp.write(encrypt_text(input_str, self._secret))

        assert Vault(self._secret).load_raw(open(fpath).read()) == expected.encode("utf-8")

    def test_encrypt_plain_text_and_write_to_file(
        self, tmp_path, Vault, decrypt_text, input_str, expected
    ):
        fpath = str((tmp_path / "vault.txt").absolute())
        with open(fpath, "w") as fp:
            Vault(self._secret).dump_raw(input_str.encode("utf-8"), fp)

        if _PY2:
            expected = expected.encode("utf-8")
        assert decrypt_text(open(fpath).read(), self._secret) == expected
