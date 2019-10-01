"""
Implement the few errors that are needed by ansible.parsing.vault as regular
exceptions.
"""


class AnsibleError(Exception):
    pass


class AnsibleAssertionError(Exception):
    pass
