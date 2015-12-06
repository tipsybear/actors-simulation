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

from gvas.config import settings
from .base import Machine

##########################################################################
# Classes
##########################################################################

class Cluster(Machine):

    def __init__(self, *args, **kwargs):
        self.racks = {}
        super(self.__class__, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, env):
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

    def add(self, node):
        """
        Adds a node to the cluster.  By default, will choose the first rack
        with available space.
        """
        pass

    def remove(self, node):
        """
        Removes a node from the cluster.
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










##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
