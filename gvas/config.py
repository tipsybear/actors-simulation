# gvas.config
# Configuration of the GVAS simulation
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Nov 05 15:05:34 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: config.py [] benjamin@bengfort.com $

"""
Configuration of the GVAS simulation
"""

##########################################################################
## Imports
##########################################################################

import os
import platform

from confire import Configuration
from confire import environ_setting
from confire import ImproperlyConfigured

##########################################################################
## Base Paths
##########################################################################

PROJECT  = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

##########################################################################
## Application Configuration
##########################################################################

class GVASSimulationConfiguration(Configuration):

    CONF_PATHS = [
        '/etc/gvas.yaml',
        os.path.expanduser('~/.gvas.yaml'),
        os.path.abspath('conf/gvas.yaml')
    ]

    debug     = False
    testing   = True


settings = GVASSimulationConfiguration.load()

if __name__ == '__main__':
    print settings
