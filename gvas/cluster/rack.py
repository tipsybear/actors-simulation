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
from .network import Network, Address

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
        self.network = Network.create(env, parent=self).next()
        super(self.__class__, self).__init__(env, *args, **kwargs)

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

    def send(self, message):
        """
        Generalized method to put message onto the contained network.
        """
        # put on internal network
        self.env.process(self._send(message))

        # determine destination rack
        rack_id = message.dst.rack
        node_id = message.dst.node

        # put on external network if needed
        if self.id != rack_id:
            dest_rack = self.cluster.racks[rack_id]
            self.env.process(
                dest_rack._send(
                    message,
                    outbound=True,
                )
            )

    def _send(self, message, outbound=False):
        """
        simpy process to simulate sending a message onto a bus and then triggering
        the recv after an appropriate latency period.
        """
        # print "Rack {}: sending message (address: {}, size: {}, value: {}) at {}\n".format(self.id, address, size, value, self.env.now)

        # reserve bandwidth to put msg on the bus
        self.network.send(message.size)

        # computed total latency
        latency = self.network.latency
        if outbound:
            latency += self.egress_latency

        # yield for required latency
        yield self.env.timeout(latency)

        # initiate recv to pick msg off the bus
        self.recv(message)

    def recv(self, message):
        """
        Generalized method to obtain a message from the contained network.
        """
        # print "Rack {}: recv message (address: {}, size: {}, value: {}) at {}\n".format(self.id, address, size, value, self.env.now)

        # de-allocate the reserved bandwidth on the bus
        self.network.recv(message.size)

        # hand off to local node if we have it otherwise ignore as outgoing traffic
        if message.dst.rack == self.id:
            self.nodes[message.dst.node].recv(message)

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
    def address(self):
        """
        Returns the rack addressable address.
        """
        return Address(self.id, None, None, None)

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
