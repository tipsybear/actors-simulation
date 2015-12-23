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

from collections import defaultdict

from gvas.base import Process
from gvas.config import settings
from gvas.utils.logger import LoggingMixin
from gvas.utils.graph import CommsGraph

from collections import deque

##########################################################################
## Module Constants
##########################################################################

DEACTIVATION_BUFFER     = settings.simulations.balance.deactivation_buffer
QUEUE_LAG               = settings.simulations.balance.queue_lag
GRAPH_COMMS             = settings.graph_comms

##########################################################################
## Actor Manager
##########################################################################

class ActorManager(Process, LoggingMixin):
    """
    The primary router and actor service for actor simulations.
    """

    def __init__(self, env, cluster):
        self.activations_requested = 0
        self.route_count = 0
        self.cluster = cluster  # The actor manager is a master process on the cluster
        self.queue   = deque()  # The message queue if there are no available actors

        # Create a Graph for communications if requested
        self.comms = CommsGraph() if GRAPH_COMMS else None

        # Init the process with the environment
        super(ActorManager, self).__init__(env)

    def _balance_up(self):
        """
        Activates inactive actors
        """
        self.logger.debug("MANAGER: ACTIVATIONS REQUESTED: {}".format(self.activations_requested))

        if self.activations_requested:
            # get a list of inactive programs
            inactive = self.filter(lambda a: not a.active)

            # activate half of what was requested
            total = self.activations_requested / 2
            for i in range(min(len(inactive), total)):
                actor = inactive[i]
                actor.activate()

            # reset counter
            self.activations_requested = 0

    def _balance_down(self):
        """
        Deactivates active actors

        if the queue is empty; deactivate actors that haven't been routed to,
        less the number of routes we had this timestep + some buffer (like 5 maybe)
        """
        self.logger.debug("MANAGER: DEACTIVATION PHASE".format())

        self.logger.debug("MESSAGE QUEUE SIZE: {}".format(len(self.queue)))
        if not self.queue:
            ready = self.filter(lambda a: a.ready)
            ready_count = len(ready)
            total_to_deactivate = ready_count - self.route_count + DEACTIVATION_BUFFER

            self.logger.debug("MANAGER: DEACTIVATING {}".format(min(total_to_deactivate, ready_count)))
            for i in range(min(total_to_deactivate, ready_count)):
                self.env.process(ready[i].deactivate())

        self.route_count = 0

    def balance(self):
        """
        Attempts to activate or deactivate the number of actors as needed.
        """
        # activate/deactivate actors as needed
        if self.activations_requested:
            self._balance_up()
        else:
            self._balance_down()

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
                # send messages if they are "old" enough
                if msg.sent < self.env.now - QUEUE_LAG:
                    self.route(msg)
                else:
                    self.queue.append(msg)

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
        # Phase one: look for an active and ready actor
        for actor in self.filter(lambda a: a.active and a.ready):
            yield actor

        # Otherwise we need to activate an actor
        for actor in self.filter(lambda a: not a.active):
            yield actor

        # No actors are available at all!
        while True:
            yield None

    def route(self, message):
        """
        Basic actor manager route method. If the message has a destination
        address, then the manager attempts to send the message to the node.
        If the node is not active, it activates it, then sends the message
        when the node is hydrated (and queues it until then).
        """
        self.route_count += 1

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
                actor.ready = False
                self.logger.debug("MANAGER: SENDING TO {}".format(actor.id))

                # Add the communication to the graph
                if GRAPH_COMMS:
                    self.comms.add_message(message)

                # Send the message and return
                return source.send(message)

            if not actor.active:
                # request an activation by the balancer
                self.logger.debug("MANAGER: REQUESTING ACTIVATION")
                self.activations_requested += 1

        # We could do nothing, so queue the message
        self.logger.debug("MANAGER: QUEUEING MESSAGE")
        message = message._replace(dst=None)
        self.queue.append(message)


class CommunicationsManager(ActorManager):

    def __init__(self, env, cluster):
        super(CommunicationsManager, self).__init__(env, cluster)
        self.activations_requested = defaultdict(int)

    def _balance_up(self):
        """
        Switches ready actors to required colors and then activates any that
        are still needed
        """
        count = 0
        self.logger.debug("BALANCE UP")
        if self.activations_requested:
            # query for ready but may not be correct color
            ready = self.filter(lambda a: a.active and a.ready)

            # query for inactive
            inactive = self.filter(lambda a: not a.active)

            # loop through requested activations by color
            for color, amount in self.activations_requested.iteritems():
                for i in range(amount):
                    if ready:
                        actor = ready.pop()
                        actor.color = color
                        self.logger.debug("MANAGER: SWITCHING COLORS: {} ({})".format(actor.id, color))
                    elif inactive:
                        # only activate every other request
                        count += 1
                        # if count % 2 == 0:
                        if True:
                            actor = inactive.pop()
                            actor.color = color
                            self.logger.debug("MANAGER: ACTIVATING: {} ({})".format(actor.id, color))
                            actor.activate()

            # reset counter
            self.activations_requested = defaultdict(int)

    def get_available_actor(self, color):
        """
        Select the next available actor in the cluster
        """
        # Phase one: look for an active and ready actor
        for actor in self.filter(lambda a: a.active and a.ready and a.color == color):
            return actor

        # Otherwise we need to activate an actor
        for actor in self.filter(lambda a: not a.active):
            return actor

        # No actors are available at all!
        return None

    def route(self, message):
        """
        Basic actor manager route method. If the message has a destination
        address, then the manager attempts to send the message to the node.
        If the node is not active, it activates it, then sends the message
        when the node is hydrated (and queues it until then).
        """
        self.route_count += 1

        # Find an available actor
        if message.dst is None:
            actor = self.get_available_actor(message.color)
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
                actor.ready = False
                self.logger.debug("MANAGER: SENDING TO {} ({})".format(actor.id, message.color))

                # Add the communication to the graph
                if GRAPH_COMMS:
                    self.comms.add_message(message)

                # Send the message and return
                return source.send(message)

            if not actor.active:
                # request an activation by the balancer
                self.logger.debug("MANAGER: REQUESTING ACTIVATION")
                self.activations_requested[message.color] += 1

        # We could do nothing, so queue the message
        self.logger.debug("MANAGER: QUEUEING MESSAGE ({})".format(message.color))
        message = message._replace(dst=None)
        self.queue.append(message)
