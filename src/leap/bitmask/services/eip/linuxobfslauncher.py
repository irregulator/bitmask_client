# -*- coding: utf-8 -*-

"""
Linux obfs launcher implementation.
"""

from leap.bitmask.config import flags


class LinuxObfsLauncher(object):
    class OBFS_BIN_PATH(object):
        def __call__(self):
            return ("/usr/local/bin/leap-obfsproxy" if flags.STANDALONE else
                    "/usr/bin/obfsproxy")
