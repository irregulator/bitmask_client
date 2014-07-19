# -*- coding: utf-8 -*-

"""
Linux obfs launcher implementation.
"""
import logging
import os
import random
import subprocess

from leap.bitmask.config import flags
from leap.bitmask.util import force_eval

logger = logging.getLogger(__name__)


class LinuxObfsLauncher(object):
    class OBFS_BIN_PATH(object):
        def __call__(self):
            return ("/usr/local/bin/leap-obfsproxy" if flags.STANDALONE
                    else "/usr/bin/obfsproxy")

    def obfs_bin_exists(self):
        try:
            import obfsproxy
        except ImportError, e:
            logger.debug(e)
            obfs_path = force_eval(self.OBFS_BIN_PATH)
            if not os.path.isfile(obfs_path):
                return False
        return True

    def pick_obfs_gw(self, obfs_list, vpn_gtw_list):
        """
        Every VPN gateway will have obfsproxy service too, but
        standalone obfsproxy servers can also be available.
        Favor a standalone obfsproxy server.
        """
        standalone_obfs = [i for i in obfs_list
                if i['ip_address'] not in vpn_gtw_list]
        if standalone_obfs:
            return random.choice(standalone_obfs)
        else:
            return random.choice(obfs_list)

    def get_obfs_args(self, obfs_gw):
        """
        Get the arguments for obfsproxy process.
        Obfsproxy will listen to a ephemeral port in
        localhost, waiting for EIP connection.
        """
        args = ['obfsproxy', '--no-log']
        args.append(obfs_gw['transport'])
        if obfs_gw['transport'] in 'scramblesuit':
            args.append('--password='+obfs_gw['scramblesuit']['password'])
        args.append('socks')
        #args.append('127.0.0.1:0')
        args.append('127.0.0.1:9989')
        return args

    def spawn_obfs(self, args):
        if flags.STANDALONE:
            subprocess.Popen(args, executable=force_eval(self.OBFS_BIN_PATH))
        else:
            subprocess.Popen(args)
