# gvas.sims.simple
# A relatively simple simulation to exercise the cluster objects.
#
# TODO:
#   - fix node address to be rack + node ids.
#   - make so that messages can travel across racks with appropriate latency.
#   - programs should spin in the send method if rack throws BandwidthExceeded
#     though its currently unclear if that would be caught. if not then
#     program should manually check the available bandwidth and spin if needed.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Sun Dec 06 12:49:03 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: filename.py [] allen.leis@gmail.com $

"""
A relatively simple simulation to exercise the cluster objects.
"""

##########################################################################
# Imports
##########################################################################

import simpy
import random

from gvas.base import Process, NamedProcess
from gvas.base import Simulation
from gvas.cluster import *
from gvas.dynamo import Uniform

##########################################################################
# Simulation Configuration
##########################################################################

# NOTE: these will come from config once sim is stable

CLUSTER_SIZE    = 1
RACK_SIZE       = 1
NODE_COUNT      = 4
START_COUNT     = 2     # number of programs to start with work phase
NODE_CPUS       = 1
NODE_MEMORY     = 4

MIN_MSG_SIZE    = 10
MAX_MSG_SIZE    = 50
MIN_MSG_VALUE   = 10
MAX_MSG_VALUE   = 50

##########################################################################
# Classes
##########################################################################

class SimpleSimulation(Simulation):

    def script(self):
        node_options = {
            'cpus': NODE_CPUS,
            'memory': NODE_MEMORY
        }
        gen = Cluster.create(
            self.env,
            size=RACK_SIZE,
            node_options=node_options
        )
        cluster = gen.next()

        # create program generator
        pgen = PingProgram.create(self.env, cpus=1, memory=4, ports=[3333, 4444])

        # create nodes using cluster's node generator
        nodes = [cluster.add() for i in range(NODE_COUNT)]

        # assign new programs to each node
        for n in nodes:
            n.assign(pgen.next())

        # set some programs to start working instead of waiting
        starters = random.sample(nodes, START_COUNT)
        work_maker = Uniform(10, 50, 'int')
        for n in starters:
            p = n.programs[n.programs.keys()[0]]
            p.work_queue.append(work_maker.next())


"""
Program needs something like a work queue (container) such that if it's working
and then receives a message, it can queue the work for the message.

Program should only wait if there are no messages/work in the queue
"""
class PingProgram(Program):

    def __init__(self, env, *args, **kwargs):
        self.work_queue = []
        self.message_size_gen = Uniform(MIN_MSG_SIZE, MAX_MSG_SIZE, 'int')
        self.message_value_gen = Uniform(MIN_MSG_VALUE, MAX_MSG_VALUE, 'int')
        self.msg_received = env.event()

        super(PingProgram, self).__init__(env, *args, **kwargs)

    def recv(self, value):
        print "Program {}: received a message with value {} at {}\n".format(self.id, value, self.env.now)
        self.work_queue.append(value)
        self.msg_received.succeed()
        self.msg_received = self.env.event()

    def wait(self):
        """
        Wait until we get a new message
        """
        print "Program {}: waiting for recv at {}\n".format(self.id, self.env.now)
        yield self.msg_received
        print "Program {}: received message! {}\n".format(self.id, self.env.now)

    def work(self):
        """
        Simulate work by going to sleep according to the oldest value in the
        work queue.
        """
        print "Program {}: starting work at {}\n".format(self.id, self.env.now)
        yield self.env.timeout(self.work_queue.pop(0))
        print "Program {}: done working at {}\n".format(self.id, self.env.now)

    def send(self):
        """
        Send a message to another node with varying size and value.  The value
        of the message will be used by the recipient computer as the amount of
        time to "work".
        """
        print "Program {}: sending at {}\n".format(self.id, self.env.now)
        yield self.env.timeout(1)

        # find other node and send the message
        recip = self.node.rack.cluster.random(
            lambda n: n.id != self.node.id and n.programs
        )
        self.node.send(
            address=recip.address,
            port=3333,
            size=self.message_size_gen.next(),
            value=self.message_value_gen.next()
        )

        print "Program {}: done sending at {}\n".format(self.id, self.env.now)

    def run(self):
        """
        Kicks off execution of a simulated program. This method contains a loop
        to cycle through specific behaviors such as:
            - wait for recv
            - sleep for random time
            - does a send to one or more other Programs/Nodes
            - repeat
        """
        while True:
            if not self.work_queue:
                waiting = self.env.process(self.wait())
                yield waiting

            working = self.env.process(self.work())
            yield working

            sending = self.env.process(self.send())
            yield sending

##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    s = SimpleSimulation()
    s.run()
