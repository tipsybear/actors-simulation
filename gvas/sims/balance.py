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
from gvas.dynamo import Stream, Normal
from gvas.cluster.network import Message
from gvas.base import Simulation, Process
from gvas.cluster import create_default_cluster
from gvas.actors import ActorProgram, ActorManager
from gvas.utils.logger import LoggingMixin

##########################################################################
## Module Constants
##########################################################################

MESSAGE_SIZE     = settings.simulations.balance.message_size
MESSAGE_MEAN     = settings.simulations.balance.message_mean
MESSAGE_STDDEV   = settings.simulations.balance.message_stddev
SPIKE_SCALE      = settings.simulations.balance.spike_scale
SPIKE_PROBABILTY = settings.simulations.balance.spike_prob
SPIKE_DURATION   = settings.simulations.balance.spike_duration

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


class BalanceActor(ActorProgram):

    def handle(self, message):
        self.logger.info("ACTOR: ID: {}, WORKING".format(self.id))
        yield self.env.timeout(1)

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
            self.diary.update('backlog', self.backlog)
            self.diary.update('incoming', self.stream.last_volume)
            # self.diary.update('ready', self.ready)
            yield self.env.timeout(1)

    @property
    def utilization(self):
        """
        Returns the percent of nodes that are utilized
        """
        nodes  = 0
        active = 0

        for node in self.cluster.nodes:
            nodes  += node.cpus
            active += sum(1 for program in node.programs.itervalues() if program.active)

        return active
        # return float(active) / float(nodes)

    @property
    def ready(self):
        """
        Returns the percent of nodes that are utilized
        """
        nodes  = 0
        ready = 0

        for node in self.cluster.nodes:
            nodes  += node.cpus
            ready += sum(1 for program in node.programs.itervalues() if program.ready)

        return ready
        # return float(active) / float(nodes)

    @property
    def backlog(self):
        """
        Returns the number of messages that are backlogged in the queue.
        """
        return len(self.manager.queue)

    def script(self):
        """
        Constructs the load balancing script for the simulation.
        """
        self.manager = ActorManager(self.env, self.cluster)
        self.stream  = StreamingData(self.env, self.manager)

        # Create actor programs for every node in the cluster.
        for node in self.cluster.nodes:
            for idx in xrange(node.cpus):
                program = BalanceActor(self.env, self.manager, ports=[idx+10, idx+20])
                node.assign(program)
