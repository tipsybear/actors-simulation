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

from gvas.base import Process, NamedProcess
from gvas.base import Simulation
from gvas.cluster import *
from gvas.dynamo import Uniform

##########################################################################
# Simulation Configuration
##########################################################################

CLUSTER_SIZE    = 1
RACK_SIZE       = 16
NODE_CPUS       = 1
NODE_MEMORY     = 4

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

        nodes = [cluster.add() for i in range(4)]
        print "Adding nodes:\n {}\n".format(nodes)

        pgen = PingProgram.create(self.env)

        p = pgen.next()
        # p.start_waiting = False
        nodes[0].assign(p)

        # nodes[1].assign(pgen.next())



"""
Program needs something like a work queue (container) such that if it's working
and then recieves a message, it can queue the work for the message.

Program should only wait if there are no messages/work in the queue
"""
class PingProgram(Program):

    def __init__(self, env, *args, **kwargs):
        self.randy = Uniform(10, 50, 'int')
        self.msg_recieved = env.event()
        self.start_waiting = kwargs.get('start_waiting', True)
        super(PingProgram, self).__init__(env, *args, **kwargs)


    def receive(self):
        self.msg_recieved.succeed()

    def wait(self):
        """
        Waits until its event is triggered.
        """

        self.msg_recieved = self.env.event()
        try:
            print "Program {}: waiting for recv at {}\n".format(self.id, self.env.now)
            yield self.env.timeout(self.randy.next())
            print "Program {}: tired of waiting {}\n".format(self.id, self.env.now)
        except simpy.Interrupt as i:
            print "Program {}: got interupted at {}\n".format(self.id, self.env.now)

    def work(self, duration=None):
        """
        Simulates work by going to sleep for a bit.
        """
        print "Program {}: starting work at {}\n".format(self.id, self.env.now)
        yield self.env.timeout(duration or self.randy.next())
        print "Program {}: done working at {}\n".format(self.id, self.env.now)

    def send(self):
        """
        Send a message to one or more nodes.
        """
        print "Program {}: sending at {}\n".format(self.id, self.env.now)
        yield self.env.timeout(1)
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
