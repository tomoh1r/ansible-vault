=============
ansible-vault
=============

This project aim to R/W an ansible-vault yaml file

(This package develop with Ansible version 1.9.1's ansible-vault.)

You can install with pip.

.. code-block:: console

   $ pip install ansible-vault

When you have an ansible-vault file, then you can read file. See below.

.. code-block:: python

   from ansible_vault import Vault

   vault = Vault('password')
   data = vault.load(open('vault.yml').read())

When you have to write data, then you can write data to file. See below.

.. code-block:: python

   from ansible_vault import Vault

   vault = Vault('password')
   vault.dump(data, open('vault.yml', 'w'))

   # also you can get encrypted text
   print(vault.dump(data))
