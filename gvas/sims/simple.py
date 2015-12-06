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
        print nodes

        pgen = PingProgram.create(self.env)
        print pgen
        p = pgen.next()


class PingProgram(Program):

    def __init__(self, env, *args, **kwargs):
        self.randy = Uniform(10, 100, 'int')

        self.wait_for_recv = self.env.Event()

        super(PingProgram, self).__init__(env, *args, **kwargs)


    def wait(self):
        """
        Part of the circle of life for this program.
        """
        print "Program {}: waiting for recv at {}".format(self.id, self.env.now)
        # duration = yield self.env.process(wait_for_recv)
        duration = yield self.env.timeout(self.randy.next())
        print "Program {}: received at {}\n".format(self.id, self.env.now)

    def work(self):
        """
        Part of the circle of life for this program.
        """
        print "Program {}: starting work at {}".format(self.id, self.env.now)
        yield self.env.timeout(self.randy.next())
        print "Program {}: done working at {}\n".format(self.id, self.env.now)

    def send(self):
        """
        Send a message to one or more nodes.
        """
        print "Program {}: sending at {}".format(self.id, self.env.now)

        # TODO: CREATE EVENT TO TRIGGER WAKEUP FOR ANOTHER NODE

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
            duration = self.wait()
            self.work(duration)
            self.send()


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    s = SimpleSimulation()
    s.run()
