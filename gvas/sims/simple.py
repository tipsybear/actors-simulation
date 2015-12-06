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

        self.wait_for_recv = self.env.Event()

        super(PingProgram, self).__init__(env, *args, **kwargs)

    def run(self):
        """
        Kicks off execution of a simulated program. This method contains a loop
        to cycle through specific behaviors such as:
            - wait for recv
            - sleep for random time
            - does a send to one or more other Programs/Nodes
            - repeat
        """
        random = Uniform(10, 100, 'int')
        while True:

            # wait random amount of time
            print "Program {}: waiting at {}".format(self.id, self.env.now)
            yield self.env.timeout(random.next())
            print "Program {}: done waiting at {}\n".format(self.id, self.env.now)

            # send to random node
            print "Program {}: sending at {}".format(self.id, self.env.now)
            yield self.env.timeout(random.next())
            print "Program {}: done sending at {}\n".format(self.id, self.env.now)


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    s = SimpleSimulation()
    s.run()
