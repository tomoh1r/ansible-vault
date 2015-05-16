=============
ansible-vault
=============

This project aim to R/W an ansible-vault yaml file

You can install with pip.

.. code-block:: console

   $ pip install ansible-vault

When you have an ansible-vault file, then you can read file. See below.

.. code-block:: python

   from ansible_vault import Vault

   vault = Vault('password')
   data = Vault.load(open('vault.yml').read())

   # if you need multilingual text, you need to encode text with utf-8.
   data = Vault.load(open('vault.yml').read().encode('utf-8'))

When you have to write data, then you can write data to file. See below.

.. code-block:: python

   from ansible_vault import Vault

   vault = Vault('password')
   Vault.dump(data, 'vault.yml')

   # also you can get encrypted text
   print(Vault.dump(data))
