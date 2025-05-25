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
import multiprocessing as mp
import os
import tempfile
from contextlib import contextmanager

from ansible.cli.vault import VaultCLI


def cli_run(args):
    """wrapper for per process calling of VaultCLI

    directory calling multiply is causes vault-id condjuction
    """
    ctx = mp.get_context("spawn")
    p = ctx.Process(target=exec_vault_cli, args=(args,))
    p.start()
    p.join()


def exec_vault_cli(args):
    cli = VaultCLI(args=args)
    cli.parse()
    cli.run()


def cli_encrypt(pass_fpath, plain_fpath, out_fpath):
    args = [
        "ansible-vault",
        "encrypt",
        "--vault-id",
        f"dev@{pass_fpath}",
        "--encrypt-vault-id",
        "dev",
        "--output",
        out_fpath,
        plain_fpath,
    ]
    cli_run(args)


def cli_decrypt(pass_fpath, vault_fpath, out_fpath):
    args = [
        "ansible-vault",
        "decrypt",
        "--vault-id",
        f"dev@{pass_fpath}",
        "--output",
        out_fpath,
        vault_fpath,
    ]
    cli_run(args)


@contextmanager
def prepare_files(content, key):
    _, content_fpath = tempfile.mkstemp()
    with open(content_fpath, "w", encoding="utf-8") as fp:
        is_bytes = isinstance(content, bytes)
        fp.write(content.decode("utf-8") if is_bytes else content)

    _, pass_fpath = tempfile.mkstemp()
    with open(pass_fpath, "w", encoding="utf-8") as fp:
        fp.write(key)

    _, out_fpath = tempfile.mkstemp()
    with open(out_fpath, "w", encoding="utf-8") as fp:
        pass

    try:
        yield (content_fpath, pass_fpath, out_fpath)
    finally:
        os.remove(out_fpath)
        os.remove(pass_fpath)
        os.remove(content_fpath)


def encrypt_text(plaintext, encrypt_key):
    with prepare_files(plaintext, encrypt_key) as (plain_fpath, pass_fpath, out_fpath):
        cli_encrypt(pass_fpath, plain_fpath, out_fpath)
        return open(out_fpath, "r", encoding="utf-8").read()


def decrypt_text(vaulttext, decrypt_key):
    with prepare_files(vaulttext, decrypt_key) as (vault_fpath, pass_fpath, out_fpath):
        cli_decrypt(pass_fpath, vault_fpath, out_fpath)
        return open(out_fpath, "r", encoding="utf-8").read()
