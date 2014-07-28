# -*- coding: utf-8 -*-

"""
Linux obfs launcher implementation.
"""
import logging
import os

from leap.bitmask.config import flags
from leap.bitmask.util import force_eval

logger = logging.getLogger(__name__)


class LinuxObfsLauncher(object):
    class OBFS_BIN_PATH(object):
        def __call__(self):
            return ("/usr/local/bin/leap-obfsproxy" if flags.STANDALONE else
                    "/usr/bin/obfsproxy")

    def obfs_bin_exists(self):
        try:
            import obfsproxy
        except ImportError, e:
            logger.debug(e)
            obfs_path = force_eval(self.OBFS_BIN_PATH)
            if not os.path.isfile(obfs_path):
                return False
        return True
