# gvas.sims.simple
# A relatively simple simulation to exercise the cluster objects.
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

CLUSTER_SIZE    = 1
RACK_SIZE       = 1
NODE_COUNT      = 32
START_COUNT     = 16     # number of programs to start with work phase
NODE_CPUS       = 1
NODE_MEMORY     = 4

MIN_MSG_SIZE    = 10
MAX_MSG_SIZE    = 50

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
        for n in starters:
            n.programs[random.choice(n.programs.keys())].start_waiting = False


"""
Program needs something like a work queue (container) such that if it's working
and then receives a message, it can queue the work for the message.

Program should only wait if there are no messages/work in the queue
"""
class PingProgram(Program):

    def __init__(self, env, *args, **kwargs):
        self.randy = Uniform(10, 50, 'int')
        self.message_sizer = Uniform(MIN_MSG_SIZE, MAX_MSG_SIZE, 'int')
        self.msg_received = env.event()
        self.start_waiting = kwargs.get('start_waiting', True)
        super(PingProgram, self).__init__(env, *args, **kwargs)

    def recv(self, size):
        print "Program {}: received a message of size {} at {}\n".format(self.id, size, self.env.now)
        self.msg_received.succeed()

    def wait(self):
        """
        Waits until its event is triggered.
        """
        try:
            print "Program {}: waiting for recv at {}\n".format(self.id, self.env.now)
            yield self.msg_received
            self.msg_received = self.env.event()
            print "Program {}: received message! {}\n".format(self.id, self.env.now)
        except simpy.Interrupt as i:
            print "Program {}: got interupted at {}\n".format(self.id, self.env.now)

    def work(self, duration=None):
        """
        Simulates work by going to sleep for a bit.
        """
        print "Program {}: starting work at {}\n".format(self.id, self.env.now)
        yield self.env.timeout(duration or self.randy.next()) | self.msg_received
        print "Program {}: done working at {}\n".format(self.id, self.env.now)

    def send(self):
        """
        Send a message to one or more nodes.
        """
        print "Program {}: sending at {}\n".format(self.id, self.env.now)
        yield self.env.timeout(1)

        # find other node and send the message
        recip = self.node.rack.cluster.random(
            lambda n: n.id != self.node.id and n.programs
        )
        self.node.send(address=recip.address, port=3333, size=50, value=100)

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
            if self.start_waiting:
                waiting = self.env.process(self.wait())
                yield waiting
            else:
                self.start_waiting = True

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
