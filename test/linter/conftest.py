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
import contextlib
import sys
from io import StringIO

import pytest


@pytest.fixture()
def capture():
    @contextlib.contextmanager
    def fn():
        bk = sys.stdout, sys.stderr
        try:
            out = [StringIO(), StringIO()]
            sys.stdout, sys.stderr = out
            yield out
        finally:
            sys.stdout, sys.stderr = bk
            out[0] = out[0].getvalue()
            out[1] = out[1].getvalue()

    return fn
