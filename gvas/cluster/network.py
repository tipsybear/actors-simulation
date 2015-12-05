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

from simpy import Container

from gvas.config import settings

##########################################################################
# Classes
##########################################################################


class Network():

    def __init__(self, *args, **kwargs):
        self._capacity = kwargs.get(
            'capacity',
            settings.defaults.network.capacity
        )
        self.medium = Container(self.env, capacity=capacity)
        super(self.__class__, self).__init__(*args, **kwargs)

    def create(self):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        pass

    def send(self, size):
        """
        Removes available bandwidth thereby simulating additional traffic on
        the network medium.
        """
        pass

    def recv(self):
        """
        Adds to available bandwidth thereby simulating removal of traffic on
        the network medium.
        """
        pass

    @property
    def bandwidth(self):
        """
        Represents the current (available) bandwidth associated with this
        resource.
        """
        pass

    @property
    def capacity(self):
        """
        Represents the maximum bandwidth associated with this resource.
        """
        return self._capacity

    @property
    def latency(self):
        """
        Computed property to return the network’s latency. This value is
        derived from the base_latency plus a function of the available
        bandwidth.
        """
        pass


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
