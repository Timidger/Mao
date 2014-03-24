# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 00:18:59 2013

@author: timidger
"""
import os
from ConfigParser import ConfigParser

config_parser = ConfigParser(allow_no_value = True)
options_file = 'options.cfg'
if not config_parser.read(options_file):
    raise IOError, 'Could not locate {} in {}'.format(options_file,
                                                      os.getcwd())
print '{} successfully loaded\n'.format(options_file)
