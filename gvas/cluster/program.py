# gvas.cluster.program
# Simulation class to model a program run within a Node instance.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:52:45 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: program.py [] allen.leis@gmail.com $

"""
Simulation class to model a program run within a Node instance.
"""

##########################################################################
# Imports
##########################################################################

from gvas.config import settings
from gvas.base import NamedProcess

##########################################################################
# Classes
##########################################################################

class Program(NamedProcess):

    def __init__(self, env, *args, **kwargs):
        self.cpus = kwargs.pop('cpus', settings.defaults.program.cpus)
        self.memory = kwargs.pop('memory', settings.defaults.program.memory)
        self.ports = kwargs.pop('ports', [])
        self.node = kwargs.pop('node', None)
        super(Program, self).__init__(env, *args, **kwargs)

    @classmethod
    def create(cls, env, *args, **kwargs):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        while True:
            yield cls(env, *args, **kwargs)

    def random_node(self):
        cluster = self.node.rack.cluster

    @property
    def id(self):
        """
        The unqiue identifier for this instance.

        Note that the _id property is initially set in the NamedProcess
        ancestor class and so all subclasses may share the same Sequence.
        """
        return self._id

    def __str__(self):
        return "Program: id: {}, cpus={},  memory={}".format(
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
    pass
