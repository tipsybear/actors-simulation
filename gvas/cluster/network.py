# gvas.cluster.network
# Simulation class to model a network resource that has available bandwidth.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:52:45 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: network.py [] allen.leis@gmail.com $

"""
Simulation class to model a network resource that has available bandwidth.
"""

##########################################################################
# Imports
##########################################################################

import simpy

from gvas.config import settings
from gvas.exceptions import BandwidthExceeded

from collections import namedtuple

##########################################################################
# Classes
##########################################################################

Message = namedtuple('Message', 'src, dst, value, size, sent, color')
Address = namedtuple('Address', 'rack, node, port, pid')


class Network(object):

    def __init__(self, env, parent=None, *args, **kwargs):
        self.parent = parent
        self.message_count = 0
        self.capacity = kwargs.get(
            'capacity',
            settings.defaults.network.capacity
        )
        self.base_latency = kwargs.get(
            'base_latency',
            settings.defaults.network.base_latency
        )
        self.medium = simpy.Container(
            env,
            init=self.capacity,
            capacity=self.capacity
        )

    @classmethod
    def create(cls, env, parent=None, *args, **kwargs):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        while True:
            yield cls(env, parent, *args, **kwargs)

    def send(self, size):
        """
        Removes available bandwidth thereby simulating additional traffic on
        the network medium.
        """
        if self.medium.level < size:
            raise BandwidthExceeded()
        self.medium.get(size)
        self.message_count += 1

    def recv(self, size):
        """
        Adds to available bandwidth thereby simulating removal of traffic on
        the network medium.
        """
        try:
            self.medium.put(size)
            self.message_count -= 1
        except ValueError:
            raise

    @property
    def bandwidth(self):
        """
        Represents the current (available) bandwidth associated with this
        resource.
        """
        return self.medium.level

    @property
    def latency(self):
        """
        Computed property to return the network's latency. This value is
        derived from the base_latency plus a function of the available
        bandwidth.
        """
        delay = 100 - int(float(self.bandwidth) / float(self.capacity) * 100)
        return self.base_latency #+ delay

    @property
    def traffic(self):
        """
        Returns the total size of messages on the network (opposite of
        bandwidth, e.g. the used bandwidth of the network).
        """
        return self.capacity - self.bandwidth

    def __str__(self):
        return "Network: capacity={},  bandwidth={}, base_latency={}, latency={}".format(
            self.capacity,
            self.bandwidth,
            self.base_latency,
            self.latency,
        )

    def __repr__(self):
        return "<{}>".format(self.__str__())


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    env = simpy.Environment()
    parent = object()

    gen = Network.create(env, parent, capacity=500)
    nw = gen.next()

    assert nw.parent, parent

    print "%r" % nw
    print "%s\n" % nw

    def tattle(x):
        print "Available bandwidth: {}".format(x.bandwidth)

    tattle(nw)
    print "Latency is at: {}\n".format(nw.latency)

    print "Sending message with size 100"
    nw.send(100)
    tattle(nw)
    print "Latency is at: {}\n".format(nw.latency)

    print "Sending message with size 100"
    nw.send(100)
    tattle(nw)
    print "Latency is at: {}\n".format(nw.latency)

    print "Receiving message with size 100"
    nw.recv(100)
    tattle(nw)
    print "Latency is at: {}\n".format(nw.latency)

    print "Receiving message with size 100"
    nw.recv(100)
    tattle(nw)
    print "Latency is at: {}\n".format(nw.latency)
