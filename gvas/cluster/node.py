# gvas.cluster.node
# Simulation class to model a compute node.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:52:45 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: node.py [] allen.leis@gmail.com $

"""
Simulation class to model a compute node.
"""

##########################################################################
# Imports
##########################################################################

import simpy

from gvas.config import settings
from gvas.exceptions import NodeLacksCapacity
from .base import Machine

##########################################################################
# Classes
##########################################################################

class Node(Machine):

    def __init__(self, env, *args, **kwargs):
        self.rack = kwargs.get('rack', None)
        self.cpus = kwargs.get('cpus', settings.defaults.node.cpus)
        self.memory = kwargs.get('cpus', settings.defaults.node.memory)
        self.programs = {}
        super(self.__class__, self).__init__(env, *args, **kwargs)

    @classmethod
    def create(cls, env, *args, **kwargs):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        while True:
            yield cls(env, *args, **kwargs)

    def send(self, address, size, value=None):
        """
        Puts a message onto the containing Rack.
        """
        pass

    def recv(self):
        """
        Obtains  a message from the containing Rack.
        """
        pass

    def assign(self):
        """
        Ingests a new Program for processing.  If there aren't enough resources
        available then raises `NodeLacksCapacity`.
        """
        pass

    def run(self):
        """
        Method to kickoff process simulation.
        """
        # TODO: replace with actual code or returned Program process
        yield self.env.timeout(1)

    @property
    def address(self):
        """
        Addressable identifier for this node containing the Rack and Node ID.
        """
        pass

    @property
    def id(self):
        """
        The unqiue identifier for this instance.

        Note that the _id property is initially set in the NamedProcess
        ancestor class and so all subclasses may share the same Sequence.
        """
        return self._id

    @property
    def idle_cpus(self):
        """
        Number of available CPUs for this node.
        """
        used = sum([p.cpus for p in self.programs.iteritems()])
        return self.cpus - used

    @property
    def idle_memory(self):
        """
        Gigabytes of available memory for this node
        """
        used = sum([p.memory for p in self.programs.iteritems()])
        return self.memory - used

    def __str__(self):
        return "Node: id: {}, cpus={},  memory={}".format(
            self.id,
            self.cpus,
            self.memory
        )

    def __repr__(self):
        return "<{}>".format(self.__str__())




##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    env = simpy.Environment()

    factory = Node.create(env, cpus=4, memory=16)
    n = factory.next()

    print n.cpus
    print n.idle_cpus
