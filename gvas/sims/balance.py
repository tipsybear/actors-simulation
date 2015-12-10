# gvas.sims.balance
# A load balancing simulation with the actor model.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Dec 09 22:23:07 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: balance.py [] benjamin@bengfort.com $

"""
A load balancing simulation with the actor model.
"""

##########################################################################
## Imports
##########################################################################

from gvas.config import settings
from gvas.base import Simulation
from gvas.cluster import create_default_cluster
from gvas.actors import ActorProgram, ActorManager


##########################################################################
## Load Balance Simulation
##########################################################################

class BalanceSimulation(Simulation):

    def __init__(self, **kwargs):
        super(BalanceSimulation, self).__init__(**kwargs)

        # Record the balance configuration in the results object.
        self.diary.configuration = settings.simulations.balance

    def setup(self):
        """
        Perform simulation-specific process setup.
        """
        # Instrument the availability and utilization in the cluster.
        self.instrumentation = self.env.process(self.instrument())

        # Create the cluster from the cluster configuration defaults.
        self.cluster = create_default_cluster(self.env)
        super(BalanceSimulation, self).setup()

    def instrument(self):
        """
        A side process that records the state of the cluster at every step.
        """
        while True:
            self.diary.update('utilization', self.utilization)
            yield self.env.timeout(1)

    @property
    def utilization(self):
        """
        Returns the percent of nodes that are utilized
        """
        nodes = 0
        idle  = 0

        for node in self.cluster.nodes:
            nodes += node.cpus
            idle += node.idle_cpus

        return float(nodes - idle) / float(nodes)

    def script(self):
        """
        Constructs the load balancing script for the simulation.
        """
        self.manager = ActorManager(self.env, self.cluster)
