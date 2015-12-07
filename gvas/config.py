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
## Nested Configurations
##########################################################################

class VisualizationConfiguration(Configuration):

    style         = "whitegrid"
    context       = "paper"
    palette       = None

##########################################################################
## Application Configuration
##########################################################################

class DefaultsConfiguration(Configuration):

    class NetworkConfiguration(Configuration):
        capacity = 1000
        base_latency = 10

    class NodeConfiguration(Configuration):
        cpus = 4
        memory = 16

    class ClusterConfiguration(Configuration):
        size = 2

    class RackConfiguration(Configuration):
        size = 96
        egress_latency = 10

    class ProgramConfiguration(Configuration):
        cpus = 1
        memory = 2

    network = NetworkConfiguration()
    cluster = ClusterConfiguration()
    rack = RackConfiguration()
    node = NodeConfiguration()
    program = ProgramConfiguration()


class GVASSimulationConfiguration(Configuration):

    CONF_PATHS    = [
        '/etc/gvas.yaml',
        os.path.expanduser('~/.gvas.yaml'),
        os.path.abspath('conf/gvas.yaml'),
        os.path.normpath('../conf/gvas.yaml'),
    ]

    debug         = False
    testing       = True

    # Visualization parameters
    vizualization = VisualizationConfiguration()

    # Global simulation parameters
    random_seed   = 42
    max_sim_time  = 1000

    defaults = DefaultsConfiguration()


settings = GVASSimulationConfiguration.load()

if __name__ == '__main__':
    print settings
