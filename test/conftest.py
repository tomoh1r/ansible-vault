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
import platform
import sys
from importlib import import_module
from textwrap import dedent

import pytest
from pkg_resources import parse_version


def pytest_addoption(parser):
    parser.addoption("--lint-code", action="store_true", help="To run linter.")


def pytest_configure(config):
    config.addinivalue_line("markers", "linter: mark test lint code.")


def pytest_runtest_setup(item):
    envnames = [mark for mark in item.iter_markers(name="linter")]
    if envnames:
        if parse_version(platform.python_version()) < parse_version("3.6"):
            pytest.skip("lint code requires python3.6 or higher.")

        if not item.config.getoption("--lint-code"):
            pytest.skip("skip lint code.")


@pytest.fixture()
def root_path():
    _here = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(_here)


@pytest.fixture()
def setup_testing_syspath(request):
    bk_syspath = sys.path
    _here = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(_here, "lib"))

    def fin():
        sys.path = bk_syspath

    request.addfinalizer(fin)


@pytest.fixture()
def testing(setup_testing_syspath):
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


@pytest.fixture(scope="session")
def ansible_ver():
    return parse_version(import_module("ansible").__version__)


@pytest.fixture()
def encrypt_text(testing):
    return testing.encrypt_text


@pytest.fixture()
def decrypt_text(testing):
    return testing.decrypt_text


@pytest.fixture(scope="function")
def vaulted_fp(tmpdir):
    # plaintext: test
    # secret: password
    fp = tmpdir.join("vault.txt")
    fp.write(
        dedent(
            """
        $ANSIBLE_VAULT;1.1;AES256
        37666535376530633739623933393737323562323336326334663130633439376165623763613339
        3765353834636336613062333638626365346438303665390a363032633262343734653461653539
        64626335383634343463616135313537346632663665366431346365323065383931376234626633
        6334396230353661340a636566396532363032363039336137323336376566303764363934333433
        6232
    """
        ).lstrip()
    )
    return fp


@pytest.fixture(scope="function")
def pwned_fp(tmpdir):
    # plaintext: !!python/object/apply:os.system ["id"]
    # secret: password
    fp = tmpdir.join("vault.txt")
    fp.write(
        dedent(
            """
        $ANSIBLE_VAULT;1.1;AES256
        31616433623434626463363932323936663066353063393731346536636437633463633137643032
        3663656431663830396662646132343735623538346330640a363532326262353732636161633431
        61353936346235396464333333653831356638393264343662363362653433353762396663653465
        6439366430336336660a363931663030323665633136363362353162333864653933653763656462
        31656431653333343834623731393263393865353831333963616165613237376630646665306363
        6238373037663462343565643737303136333032386136356438
    """
        ).lstrip()
    )
    return fp
