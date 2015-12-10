# gvas.actors.manager
# Service for generalized actors, performs load balancing and maintains stage.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Dec 09 22:10:28 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: manager.py [] benjamin@bengfort.com $

"""
Service for generalized actors, performs load balancing and maintains stage.
"""

##########################################################################
## Imports
##########################################################################

from gvas.base import Process
from gvas.utils.logger import LoggingMixin

from collections import deque

##########################################################################
## Actor Manager
##########################################################################

class ActorManager(Process, LoggingMixin):
    """
    The primary router and actor service for actor simulations.
    """

    def __init__(self, env, cluster):
        # The actor manager is a master process on the cluster
        self.cluster = cluster
        self.queue   = deque()
        super(ActorManager, self).__init__(env)

    def run(self):
        """
        Go through the queue, attempting to assign queued messages to nodes.
        """
        while True:
            # Create temporary queue
            queue = list(self.queue)
            self.queue.clear()

            for msg in queue:
                self.route(msg)

            yield self.env.timeout(1)

    def actors(self):
        """
        Iterator for all of the actors in the cluster.
        """
        for node in self.cluster.nodes:
            for program in node.programs.itervalues():
                yield program

    def filter(self, evaluator):
        """
        Filter actors by a functional criteria
        """
        return filter(evaluator, self.actors())

    def get_available_actor(self):
        """
        Select the next available actor in the cluster
        """
        for actor in self.filter(lambda a: a.active and a.ready):
            return actor

        # Otherwise we need to rehydrate an actor
        for actor in self.filter(lambda a: not a.active):
            return actor

        return None

    def route(self, msg):
        """
        Basic actor manager route method. If the message has a destination
        address, then the manager attempts to send the message to the node.
        If the node is not active, it activates it, then sends the message
        when the node is hydrated (and queues it until then).
        """

        # Find an available actor
        if msg.dst is None:
            actor = self.get_available_actor()
            if actor is not None:
                msg = msg._replace(dst="{}:{}".format(actor.node.address, actor.ports[0]))

        # attempt to send the message
        if msg.dst is not None:
            drack, dnode, dport = map(int, msg.dst.split(":"))
            actor = self.cluster.racks[drack].nodes[dnode].programs[dport]
            if actor.active and actor.ready:
                # send the message!
                addr = "{}:{}".format(drack, dnode)

                if msg.src is not None:
                    srack, snode, sport = map(int, msg.dst.split(":"))
                    self.cluster.racks[srack].nodes[snode].send(
                        addr, dport, msg.size, msg.value
                    )
                else:
                    self.cluster.racks[drack].send(
                        addr, dport, msg.size, msg.value
                    )

                # Job done, lets bail!
                return
            else:
                # reinsantiate the actor
                actor.activate()

        # We could do nothing, so queue the message
        self.queue.append(msg)
