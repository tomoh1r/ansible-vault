import os
from tempfile import mkstemp

from testfixtures import ShouldRaise

from ansible.errors import AnsibleError


here = os.path.dirname(os.path.abspath(__file__))


class TestVaultLoad(object):
    def _getTargetClass(self):
        from ansible_vault import Vault
        return Vault

    def _makeOne(self, password):
        return self._getTargetClass()(password)

    def test_can(self):
        fpath = os.path.join(here, 'file', 'vault.txt')
        vault = self._makeOne('password')
        assert vault.load(open(fpath).read()) == 'test'

    def test_cannot(self):
        fpath = os.path.join(here, 'file', 'vault.txt')
        vault = self._makeOne('invalid-password')
        with ShouldRaise(AnsibleError('Decryption failed')):
            vault.load(open(fpath).read())


class TestVaultDump(object):
    def _getTargetClass(self):
        from ansible_vault import Vault
        return Vault

    def _makeOne(self, password):
        return self._getTargetClass()(password)

    def test_dump_file(self):
        fpath = mkstemp()[1]
        with open(fpath, 'w+b') as fp:
            write_vault = self._makeOne('password')
            write_vault.dump('test', fp)

        with open(fpath, 'r+b') as fp:
            read_vault = self._makeOne('password')
            assert read_vault.load(fp.read()) == 'test'

        os.remove(fpath)

    def test_dump_text(self):
        write_vault = self._makeOne('password')
        dumped = write_vault.dump('test')

        read_vault = self._makeOne('password')
        assert read_vault.load(dumped) == 'test'
