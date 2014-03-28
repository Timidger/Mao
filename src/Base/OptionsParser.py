# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 00:18:59 2013

@author: timidger
"""
import os
from ConfigParser import ConfigParser


def load_configuration(file_name):
    """In the current directory, the configuration file named file_name is
    loaded and returned in a ConfigParser"""
    config_parser = ConfigParser(allow_no_value=True)
    if not file_name.endswith(".cfg"):
        file_name += ".cfg"
    if not config_parser.read(file_name):
        raise(IOError,
              'Could not locate {} in {}'.format(file_name, os.getcwd()))
    return config_parser
