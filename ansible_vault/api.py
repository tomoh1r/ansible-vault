import yaml
try:
    from ansible.utils.vault import VaultLib
except ImportError:
    # Ansible 2.0 has changed the vault location
    from ansible.parsing.vault import VaultLib


class Vault(object):
    '''R/W an ansible-vault yaml file'''

    def __init__(self, password):
        self.password = password
        self.vault = VaultLib(password)

    def load(self, stream):
        '''read vault steam and return python object'''
        return yaml.load(self.vault.decrypt(stream))

    def dump(self, data, stream=None):
        '''encrypt data and print stdout or write to stream'''
        yaml_text = yaml.dump(
            data,
            default_flow_style=False,
            allow_unicode=True)
        encrypted = self.vault.encrypt(yaml_text)
        if stream:
            stream.write(encrypted)
        else:
            return encrypted
