# gvas.sims.comuunications
# A simulation that can model different communication patterns.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Dec 09 22:23:07 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: communications.py [] benjamin@bengfort.com $

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
# from gvas.actors import ActorProgram, ActorManager
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

##########################################################################
## Data Generator (Stream)
##########################################################################

class StreamingData(Process, LoggingMixin):
    """
    Generates data volume via the stream dynamo.

    TODO: Move out of simulation to a helper module.
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
                    self.service.route(Message(None, None, self.values.get(), MESSAGE_SIZE, self.env.now))

            self.last_volume = volume
            yield self.env.timeout(1)

##########################################################################
## Load Balance Simulation
##########################################################################



class CommunicationsSimulation(BalanceSimulation):
    pass
