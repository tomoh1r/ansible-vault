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

import os
from importlib import import_module

import pytest


@pytest.mark.linter
def test_pylint(chdir_root_path):
    cmd = ". --rcfile={} --score=no".format(os.path.abspath(".pylintrc"))
    stdout, stderr = import_module("pylint.epylint").py_run(cmd, return_std=True)
    stdout, stderr = stdout.getvalue(), stderr.getvalue()
    assert "" == stdout, stdout
