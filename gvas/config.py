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
        node_count = 64

    class RackConfiguration(SerializableConfiguration):
        size = 32
        egress_latency = 10

    class ProgramConfiguration(SerializableConfiguration):
        cpus = 1
        memory = 2

    class ActorsConfiguration(SerializableConfiguration):
        persistence_cost = 2


    network = NetworkConfiguration()
    cluster = ClusterConfiguration()
    rack = RackConfiguration()
    node = NodeConfiguration()
    program = ProgramConfiguration()
    actors = ActorsConfiguration()


class SimulationsConfiguration(SerializableConfiguration):

    class SimpleSimulationConfiguration(SerializableConfiguration):
        node_count = 8
        start_team_size = 4

        min_msg_size = 10
        max_msg_size = 50
        min_msg_value = 10
        max_msg_value = 50

    class BalanceSimulationConfiguration(SerializableConfiguration):

        volume_threshold = 100
        message_size     = 128
        spike_prob       = 0.05
        spike_duration   = 15
        spike_scale      = 5
        message_mean     = 16
        message_stddev   = 8

    simple = SimpleSimulationConfiguration()
    balance = BalanceSimulationConfiguration()

##########################################################################
## Logging Configuration
##########################################################################

class LoggingConfiguration(Configuration):
    """
    Very specific logging configuration instructions (does not provide the
    complete configuration as available in the python logging module). See
    the `gvas.utils.logger` module for more info.
    """

    level   = "INFO"
    logfmt  = "[%(time)5d] %(message)s"
    datefmt = "%Y-%m-%dT%H:%M:%S%z"
    disable_existing_loggers = False


##########################################################################
## Application Configuration
##########################################################################

class GVASSimulationConfiguration(Configuration):

    CONF_PATHS    = [
        '/etc/gvas.yaml',
        os.path.expanduser('~/.gvas.yaml'),
        os.path.abspath('conf/gvas.yaml'),
        os.path.normpath('../conf/gvas.yaml'),
    ]

    debug         = False
    testing       = False

    # Visualization parameters
    vizualization = VisualizationConfiguration()

    # Global simulation parameters
    random_seed   = 42
    max_sim_time  = 1000

    # Logging parameters
    logging       = LoggingConfiguration()

    defaults      = DefaultsConfiguration()
    simulations   = SimulationsConfiguration()

##########################################################################
## Construct settings for use in the library.
##########################################################################

settings = GVASSimulationConfiguration.load()

if __name__ == '__main__':
    print settings
