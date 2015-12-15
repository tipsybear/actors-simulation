# gvas.cluster
# Simulation classes to model distributed system components.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:48:51 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: __init__.py [] allen.leis@gmail.com $

"""
Simulation classes to model distributed system components.
"""

##########################################################################
# Imports
##########################################################################

from .cluster import Cluster
from .rack import Rack
from .node import Node
from .program import Program

from gvas.config import settings

##########################################################################
# Utility to generate a default cluster
##########################################################################

CLUSTER_SIZE    = settings.defaults.cluster.size
RACK_SIZE       = settings.defaults.rack.size
NODE_CPUS       = settings.defaults.node.cpus
NODE_MEMORY     = settings.defaults.node.memory
NODE_COUNT      = settings.defaults.cluster.node_count

def default_cluster_generator(env, **kwargs):
    """
    Helper function for generating default clusters from the settings.
    """
    rack_options = {
        'size': kwargs.get('rsize', RACK_SIZE)
    }

    node_options = {
        'cpus': kwargs.get('cpus', NODE_CPUS),
        'memory': kwargs.get('memory', NODE_MEMORY)
    }

    return Cluster.create(
        env,
        size=kwargs.get('csize', CLUSTER_SIZE),
        rack_options=rack_options,
        node_options=node_options,
    )


def create_default_cluster(env, **kwargs):
    """
    Helper function to simply return a cluster.
    """
    generator = default_cluster_generator(env, **kwargs)
    cluster = generator.next()

    # Add nodes
    for _ in xrange(kwargs.get('node_count', NODE_COUNT)):
        cluster.add()

    return cluster
