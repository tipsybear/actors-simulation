# gvas.sims.comuunications
# A simulation that can model different communication patterns.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Thu Dec 17 01:37:35 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: communications.py [] allen.leis@gmail.com $

"""
A simulation that can model different communication patterns.
"""

##########################################################################
## Imports
##########################################################################

from gvas.config import settings
from gvas.dynamo import Stream, Normal
from gvas.cluster.network import Message
from gvas.base import Simulation, Process
from gvas.cluster import create_default_cluster
from gvas.actors import BlueActor, CommunicationsManager
from gvas.utils.logger import LoggingMixin
from .balance import BalanceSimulation

##########################################################################
## Module Constants
##########################################################################

MESSAGE_SIZE     = settings.simulations.communications.message_size
MESSAGE_MEAN     = settings.simulations.communications.message_mean
MESSAGE_STDDEV   = settings.simulations.communications.message_stddev
SPIKE_SCALE      = settings.simulations.communications.spike_scale
SPIKE_PROBABILTY = settings.simulations.communications.spike_prob
SPIKE_DURATION   = settings.simulations.communications.spike_duration
INITIAL_COLOR    = settings.simulations.communications.initial_color

##########################################################################
## Data Generator (Stream)
##########################################################################

class StreamingData(Process, LoggingMixin):
    """
    Generates data volume via the stream dynamo.
    """

    def __init__(self, env, service, **kwargs):
        """
        Takes an environment and an actor service, and streams data to it.
        """
        self.service = service
        self.stream  = Stream(MESSAGE_MEAN, MESSAGE_STDDEV, SPIKE_SCALE, SPIKE_PROBABILTY, SPIKE_DURATION)
        self.values  = Normal(64, 32)
        self.last_volume = 0
        super(StreamingData, self).__init__(env)

    def run(self):
        """
        Creates messages based on the data volume and sends to the service.
        """

        # Don't start for a few iterations
        yield self.env.timeout(5)

        while True:
            volume = int(self.stream.next())
            if volume > 0:
                self.logger.info("STREAM: NEW MESSAGES: {}".format(volume))
                for idx in xrange(volume):
                    self.service.route(Message(None, None, self.values.get(), MESSAGE_SIZE, self.env.now, INITIAL_COLOR))

            self.last_volume = volume
            yield self.env.timeout(1)

##########################################################################
## Load Balance Simulation
##########################################################################

class CommunicationsSimulation(BalanceSimulation):

    def instrument(self):
        """
        A side process that records the state of the cluster at every step.
        """
        while True:
            self.diary.update('utilization', self.utilization)
            self.diary.update('backlog', self.backlog)
            self.diary.update('incoming', self.stream.last_volume)
            yield self.env.timeout(1)

    def script(self):
        """
        Constructs the load balancing script for the simulation.
        """
        self.manager = CommunicationsManager(self.env, self.cluster)
        self.stream  = StreamingData(self.env, self.manager)

        # Create actor programs for every node in the cluster.
        for node in self.cluster.nodes:
            for idx in xrange(node.cpus):
                program = BlueActor(self.env, self.manager, ports=[idx+10, idx+20])
                node.assign(program)
