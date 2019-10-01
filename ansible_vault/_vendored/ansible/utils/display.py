"""
Implement a dummy Display class that simply logs its messages to a Python logger.
"""

import logging

logger = logging.getLogger("ansible_vault._vendored.ansible")


class Display(object):
    def prompt(self):
        raise RuntimeError("Not implemented.")

    def vvvv(self, msg):
        logger.info(msg)

    def vvvvv(self, msg):
        logger.debug(msg)
