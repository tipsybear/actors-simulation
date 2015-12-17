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
        self.cluster = cluster # The actor manager is a master process on the cluster
        self.queue   = deque() # The message queue if there are no available actors
        super(ActorManager, self).__init__(env)

    def balance(self):
        """
        calls deactivate on unnescessary actors
        """
        pass

    def run(self):
        """
        Go through the queue, attempting to assign queued messages to nodes.
        """
        while True:
            # Create temporary queue
            self.queue.reverse()
            queue = list(self.queue)
            self.queue.clear()

            # Availability
            self.available = self.get_available_actors()

            for msg in queue:
                if msg.sent < self.env.now:
                    self.route(msg)

            # Send deactivate message to actors if needed
            self.balance()

            yield self.env.timeout(1)

    def lookup(self, address):
        """
        Lookup an actor by address. Returns None if it cannot find an actor
        at the specified address.
        """
        rack = self.cluster.racks.get(address.rack, {})
        node = rack.nodes.get(address.node, {})
        return node.programs.get(address.pid, None)

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

    def get_available_actors(self):
        """
        Select the next available actor in the cluster
        """
        while True:
            # Phase one: look for an active and ready actor
            for actor in self.filter(lambda a: a.active and a.ready):
                yield actor

            # Otherwise we need to activate an actor
            for actor in self.filter(lambda a: not a.active):
                yield actor

            # No actors are available at all!
            yield None

    def route(self, message):
        """
        Basic actor manager route method. If the message has a destination
        address, then the manager attempts to send the message to the node.
        If the node is not active, it activates it, then sends the message
        when the node is hydrated (and queues it until then).
        """

        # Find an available actor
        if message.dst is None:
            actor = self.available.next()
            if actor is not None:
                message = message._replace(dst=actor.address)

        # attempt to send the message
        if message.dst is not None:
            actor = self.lookup(message.dst)
            if actor is None: raise Exception(message.dst)
            if actor.active and actor.ready:
                # send the message!
                if message.src is not None:
                    source = self.cluster.racks[message.src.rack]
                    source = source.nodes[message.src.node]
                else:
                    source = self.cluster.racks[message.dst.rack]

                # Mark actor as queued and send the message
                # If you comment out the below lines, then the streaming data
                # service doesn't stall. What's going on here?
                actor.ready = False
                return source.send(message)

            if not actor.active:
                # activate the actor!
                actor.activate()

        # We could do nothing, so queue the message
        message = message._replace(dst=None)
        self.queue.append(message)
