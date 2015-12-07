# gvas.cluster.rack
# Simulation class to model an enclosure for physical computers.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:50:27 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: rack.py [] allen.leis@gmail.com $

"""
Simulation class to model an enclosure for physical computers.
"""

##########################################################################
# Imports
##########################################################################

from gvas.config import settings
from gvas.exceptions import RackLacksCapacity
from .base import Machine
from .node import Node

##########################################################################
# Classes
##########################################################################

class Rack(Machine):

    def __init__(self, env, *args, **kwargs):
        self.cluster = kwargs.get('cluster', None)
        node_options = kwargs.get('node_options', {})
        self.node_generator = kwargs.get(
            'node_generator',
            Node.create(env, **node_options)
        )
        self.size = kwargs.get(
            'size',
            settings.defaults.rack.size
        )
        self.egress_latency = kwargs.get(
            'egress_latency',
            settings.defaults.rack.egress_latency
        )
        self.nodes = {}
        super(self.__class__, self).__init__(env, *args, **kwargs)

    @classmethod
    def create(cls, env, *args, **kwargs):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        while True:
            yield cls(env, *args, **kwargs)

    def filter(self, evaluator):
        """
        Uses the evaluator function to test against the Node instances and
        return a list of matches.
        """
        pass

    def first(self, evaluator):
        """
        Uses the evaluator function to test against the Node instances and
        return the first match.
        """
        pass

    def send(self, address, port, size, value=None):
        """
        Generalized method to put message onto the contained network.
        """
        print "Rack {}: sending message at {}\n".format(self.id, self.env.now)
        self.network.send(size)

        yield self.env.timeout(self.network.latency)
        self.recv(address=address, port=port, size=size, value=value)

    def recv(self, address, port, size, value=None):
        """
        Generalized method to obtain a message from the contained network.
        """
        print "Rack {}: delivering (recv) message at {}\n".format(self.id, self.env.now)
        self.network.recv(size)
        self.nodes[address].recv(port=port, size=size, value=value)

    def add(self, node=None):
        """
        Adds a node to the cluster.  By default, will choose the first rack
        with available space. If no node was passed, then use internal Node
        generator.
        """
        if self.space < 1:
            raise RackLacksCapacity()

        if not node:
            node = self.node_generator.next()

        self.nodes[node.id] = node
        node.rack = self

    def remove(self, node):
        """
        Removes a node from the cluster.
        """
        # for funsies, return the removed node or None if it wasnt found.
        return self.nodes.pop(node.id, None)

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
    def space(self):
        """
        Convenience property to return computed space available for more nodes.
        """
        return self.size - len(self.nodes)

    @property
    def full(self):
        """
        Convenience property to determine whether rack is at capacity.
        """
        return self.size <= len(self.nodes)

    def __str__(self):
        return "Rack: id: {}, size={},  nodes={}".format(
            self.id,
            self.size,
            len(self.nodes)
        )

    def __repr__(self):
        return "<{}>".format(self.__str__())


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
