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

from gvas.config import settings
from gvas.exceptions import NodeLacksCapacity
from .base import Machine

##########################################################################
# Classes
##########################################################################

class Node(Machine):

    def __init__(self, *args, **kwargs):
        self.rack = kwargs.get('rack', None)
        self.programs = {}
        super(self.__class__, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, env):
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
    def cpus(self):
        """
        Number of CPUs for this node.
        """
        pass

    @property
    def memory(self):
        """
        Gigabytes of memory for this node
        """
        pass

    @property
    def idle_cpus(self):
        """
        Number of available CPUs for this node.
        """
        pass

    @property
    def idle_memory(self):
        """
        Gigabytes of available memory for this node
        """
        pass




##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
