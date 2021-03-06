# gvas.cluster.cluster
# Simulation class to model a cluster of resources.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:50:27 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: cluster.py [] allen.leis@gmail.com $

"""
Simulation class to model a cluster of resources.
"""

##########################################################################
# Imports
##########################################################################

import random

from gvas.config import settings
from gvas.exceptions import ClusterLacksCapacity
from .base import Machine
from .rack import Rack
from .node import Node

##########################################################################
# Classes
##########################################################################

class Cluster(Machine):

    def __init__(self, env, *args, **kwargs):
        rack_options = kwargs.get('rack_options', {})
        node_options = kwargs.get('node_options', {})
        self.rack_generator = kwargs.get(
            'rack_generator',
            Rack.create(
                env,
                cluster=self,
                node_options=node_options,
                **rack_options
            )
        )
        self.size = kwargs.get(
            'size',
            settings.defaults.cluster.size
        )
        node_options = kwargs.get('node_options', {})
        self.node_generator = kwargs.get(
            'node_generator',
            Node.create(env, **node_options)
        )

        racks = [self.rack_generator.next() for i in range(self.size)]
        self.racks = dict((r.id, r) for r in racks)
        super(self.__class__, self).__init__(env, *args, **kwargs)        

    def filter(self, evaluator):
        """
        Uses the evaluator function to test against the Node instances and
        return a list of matches.
        """
        return filter(evaluator, self.nodes)

    def first(self, evaluator):
        """
        Uses the evaluator function to test against the Node instances and
        return the first match.
        """
        for n in self.nodes:
            if evaluator(n):
                return n
        return None

    def random(self, evaluator=lambda n: True):
        """
        Uses the evaluator function to test against the Node instances and
        return a random match.
        """
        return random.choice(self.filter(evaluator))

    def send(self, *args, **kwargs):
        """
        Generalized method to put message onto the contained network.
        """
        pass

    def recv(self, *args, **kwargs):
        """
        Generalized method to obtain a message from the contained network.
        """
        pass

    def add(self, node=None, rack=None, rack_id=None):
        """
        Adds a node to the cluster.  Will add the node to the specified rack or
        rack_id.  Otherwise, will choose the first rack with available space.
        """
        if not rack:
            if rack_id:
                rack = self.racks[rack_id]
            rack = self.first_available_rack

        if not node:
            node = self.node_generator.next()

        rack.add(node)
        return node


    def remove(self, node):
        """
        Removes a node from the cluster.
        """
        pass

    def run(self):
        """
        Method to kickoff process simulation.
        """
        yield self.env.timeout(1)

    @property
    def id(self):
        """
        The unqiue identifier for this instance.

        Note that the _id property is initially set in the NamedProcess
        ancestor class and so all subclasses may share the same Sequence.
        """
        return self._id

    @property
    def nodes(self):
        """
        Returns a generator to iterate through all of the nodes in the racks.
        """
        for r in self.racks.itervalues():
            for n in r.nodes.itervalues():
                yield n

    @property
    def first_available_rack(self):
        """
        Returns the first rack with room for a node or raises
        ClusterLacksCapacity.
        """
        ids = sorted(self.racks.keys())

        for id in ids:
            if not self.racks[id].full:
                return self.racks[id]

        raise ClusterLacksCapacity()

    def get_message_count(self):
        """
        Returns the number of messages on the network
        """
        return sum(
            r.network.message_count for r in self.racks.itervalues()
        )

    def get_total_message_size(self):
        """
        Returns the total size of the messages on the network
        """
        return sum(
            r.network.traffic for r in self.racks.itervalues()
        )

    def get_total_latency(self):
        """
        Returns the total latency of the network
        """
        return sum(
            r.network.latency for r in self.racks.itervalues()
        )

    def get_average_latency(self):
        """
        Returns the mean latency of the network
        """
        return self.get_total_latency() / float(len(self.racks))

    def get_total_bandwidth(self):
        """
        Returns the total bandwidth of the network
        """
        return sum(
            r.network.bandwidth for r in self.racks.itervalues()
        )

    def get_average_bandwidth(self):
        """
        Returns the mean latency of the network
        """
        return self.get_total_bandwidth() / float(len(self.racks))


    def __str__(self):
        nodes = sum([len(r.nodes) for r in self.racks.itervalues()])
        return "Cluster: id: {}, racks={},  nodes={}".format(
            self.id,
            self.size,
            nodes
        )

    def __repr__(self):
        return "<{}>".format(self.__str__())

##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
