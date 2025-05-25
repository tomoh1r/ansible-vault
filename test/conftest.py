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
import os
import sys
from importlib import import_module

import pytest

here = os.path.dirname(os.path.abspath(__file__))


def pytest_addoption(parser):
    parser.addoption("--lint-code", action="store_true", help="To run linter.")


def pytest_configure(config):
    config.addinivalue_line("markers", "linter: mark test lint code.")


def pytest_runtest_setup(item):
    envnames = [mark for mark in item.iter_markers(name="linter")]
    if envnames:
        if not item.config.getoption("--lint-code"):
            pytest.skip("skip lint code.")


@pytest.fixture()
def root_path():
    return os.path.dirname(here)


@pytest.fixture()
def chdir_root_path(monkeypatch, root_path):
    monkeypatch.chdir(root_path)


@pytest.fixture(scope="session", autouse=True)
def setup_testing_syspath(request):
    bk_syspath = sys.path
    _here = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(_here, "lib"))

    def fin():
        sys.path = bk_syspath

    request.addfinalizer(fin)


@pytest.fixture()
def testing():
    return import_module("testing")


@pytest.fixture()
def Vault():
    return import_module("ansible_vault").Vault


@pytest.fixture()
def VaultLib():
    try:
        return import_module("ansible.parsing.vault").VaultLib
    except ImportError:
        # Ansible<2.0
        return import_module("ansible.utils.vault").VaultLib


@pytest.fixture(scope="function")
def vaulted_fp():
    # plaintext: test
    # secret: password
    fpath = os.path.join(here, "file", "vault.txt")
    return open(fpath, "r", encoding="utf-8")


@pytest.fixture(scope="function")
def pwned_fp():
    # plaintext: !!python/object/apply:os.system ["id"]
    # secret: password
    fpath = os.path.join(here, "file", "pwned.txt")
    return open(fpath, "r", encoding="utf-8")
