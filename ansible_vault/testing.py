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
import sys
import os
import shlex
import subprocess
import tempfile


class AnsibleVaultExecutor(object):
    def get_version(self):
        import ansible
        return float('.'.join(ansible.__version__.split('.')[:2]))

    def get_executor(self):
        return os.path.join(os.path.dirname(sys.executable), 'ansible-vault')

    def encrypt(self, pass_path, plain_fpath):
        pass_opt = 'vault-password-file'
        if self.get_version() >= 2.4:
            pass_opt = 'vault-id'

        args = ('encrypt --{pass_opt}={pass_path} {plain_fpath}'
                .format(pass_opt=pass_opt,
                        pass_path=pass_path,
                        plain_fpath=plain_fpath))
        subprocess.check_output(
            shlex.split(' '.join([self.get_executor(), args])))

    def decrypt(self, pass_path, vault_fpath):
        pass_opt = 'vault-password-file'
        if self.get_version() >= 2.4:
            pass_opt = 'vault-id'

        args = ('decrypt --{pass_opt}={pass_path} {vault_fpath}'
                .format(pass_opt=pass_opt,
                        pass_path=pass_path,
                        vault_fpath=vault_fpath))
        subprocess.check_output(
            shlex.split(' '.join([self.get_executor(), args])))


def encrypt_text(plaintext, secret, vault_id=None):
    _, plain_fpath = tempfile.mkstemp()
    with open(plain_fpath, 'w') as fp:
        fp.write(plaintext)

    _, pass_path = tempfile.mkstemp()
    with open(pass_path, 'w') as fp:
        fp.write(secret)

    try:
        AnsibleVaultExecutor().encrypt(pass_path, plain_fpath)

        with open(plain_fpath) as fp:
            return fp.read()

    finally:
        os.remove(pass_path)
        os.remove(plain_fpath)


def decrypt_text(vaulttext, secret):
    _, vault_fpath = tempfile.mkstemp()
    with open(vault_fpath, 'w') as fp:
        if isinstance(vaulttext, bytes):
            vaulttext = vaulttext.decode('utf-8')
        fp.write(vaulttext)

    _, pass_path = tempfile.mkstemp()
    with open(pass_path, 'w') as fp:
        fp.write(secret)

    try:
        AnsibleVaultExecutor().decrypt(pass_path, vault_fpath)

        with open(vault_fpath) as fp:
            return fp.read()

    finally:
        os.remove(pass_path)
        os.remove(vault_fpath)
