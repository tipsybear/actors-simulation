# gvas.cluster.base
# Base classes for cluster simulation framework.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:49:32 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: base.py [] allen.leis@gmail.com $

"""
Base classes for cluster simulation framework.
"""

##########################################################################
# Imports
##########################################################################

from six import with_metaclass
from abc import ABCMeta
from abc import abstractmethod, abstractproperty

from gvas.base import NamedProcess

##########################################################################
# Classes
##########################################################################

class Machine(with_metaclass(ABCMeta, NamedProcess)):

    @abstractmethod
    def create(self, *args, **kwargs):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        pass

    @abstractmethod
    def send(self, *args, **kwargs):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        pass

    @abstractmethod
    def recv(self, *args, **kwargs):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        pass

    @property
    def network(self):
        """
        Returns a reference to the underlying Network instance
        """
        return self._network


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
