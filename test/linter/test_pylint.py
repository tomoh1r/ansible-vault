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
from io import StringIO
from pathlib import Path

import pytest
from pylint import lint


@pytest.mark.linter
def test_pylint(chdir_root_path):
    """
    Run Pylint against the project root, using .pylintrc, and
    assert that no errors are reported.
    """
    # Path to your pylintrc
    _parent = Path(__file__).parent.parent.parent.absolute()
    rcfile = str(_parent / ".pylintrc")

    # Prepare arguments for lint.Run: [--rcfile, path, --score, no, target]
    srcpath = str(_parent / "ansible_vault")
    testpath = str(_parent / "test" / "*")
    args = ["--rcfile", rcfile, "--score", "no", srcpath, testpath]

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
