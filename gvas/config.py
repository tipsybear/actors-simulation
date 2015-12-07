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
## Serializable Configuration -- for writing Config as Results
##########################################################################

class SerializableConfiguration(Configuration):

    def serialize(self):
        return dict(self.options())

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

class DefaultsConfiguration(SerializableConfiguration):

    class NetworkConfiguration(SerializableConfiguration):
        capacity = 1000
        base_latency = 10

    class NodeConfiguration(SerializableConfiguration):
        cpus = 4
        memory = 16

    class ClusterConfiguration(SerializableConfiguration):
        size = 2

    class RackConfiguration(SerializableConfiguration):
        size = 96
        egress_latency = 10

    class ProgramConfiguration(SerializableConfiguration):
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
