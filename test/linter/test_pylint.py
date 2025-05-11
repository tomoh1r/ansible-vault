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
import os
import sys
from io import StringIO

import pytest
from pylint import lint


@pytest.mark.linter
def test_pylint(chdir_root_path):
    """
    Run Pylint against the project root, using .pylintrc, and
    assert that no errors are reported.
    """
    # Path to your pylintrc
    rcfile = os.path.abspath(".pylintrc")

    # Prepare arguments for lint.Run: [--rcfile, path, --score, no, target]
    args = ["--rcfile", rcfile, "--score", "no", "."]

    # Capture stdout/stderr
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = StringIO()

    # Run Pylint without exiting the process
    result = lint.Run(args, exit=False)

    # Retrieve output and restore streams
    output = sys.stdout.getvalue()
    sys.stdout, sys.stderr = old_stdout, old_stderr

    # Assert that Pylint found no issues (exit status 0)
    assert result.linter.msg_status == 0, f"Pylint errors:\n{output}"
