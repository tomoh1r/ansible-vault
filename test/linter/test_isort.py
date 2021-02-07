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
from __future__ import absolute_import, unicode_literals

from importlib import import_module

import pytest


@pytest.mark.linter
def test_isort(monkeypatch, root_path, capture):
    monkeypatch.chdir(root_path)

    with capture() as out:
        try:
            import_module("isort.main").main(argv=["--check-only", "."])
        except SystemExit:
            pass

    assert "ERROR" not in out[1], "Please run `./venv/bin/python3 -m isort .`."
