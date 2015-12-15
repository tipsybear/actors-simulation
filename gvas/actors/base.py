# gvas.actors.base
# The base actors program for simulating actor behavor on the cluster.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Dec 09 15:44:59 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
The base actors program for simulating actor behavor on the cluster.
"""

##########################################################################
## Imports
##########################################################################

from gvas.cluster import Program
from gvas.config import settings

##########################################################################
## Actor simulation configuration
##########################################################################

SEND_LATENCY     = 1
PERSISTENCE_COST = settings.defaults.actors.persistence_cost

##########################################################################
## Actor Program
##########################################################################

class ActorProgram(Program):
    """
    An actor simulation is composed of one more more actor programs, whose
    class defines a method of actor operation, and where multiple instances
    provide concurrency on the cluster.
    """

    def __init__(self, env, manager, *args, **kwargs):
        # The manager is the GVAS actor service and is required.
        self.manager    = manager

        self.ready      = False  # Ready to receive a message
        self.active     = False  # Active or inactive state
        self.checkpoint = False  # Require a persist on the next go around
        self.message    = None   # Message channel to listen for messages
        self.hydrate    = None   # Activation channel to listen for activations
        self.outbox     = []     # Handle puts messages on the outbox to send

        super(ActorProgram, self).__init__(env, *args, **kwargs)

    def handle(self, message):
        """
        Actor programs are continually listening for a message, upon receipt
        of a message the actor program can do one of the following things:

            1. Change state (variable cost, "work")
            2. Send messages to other actors (actor types)
            3. Persist its state (static cost)

        The message sending pattern is the only real difference in many types
        of actor based simulations, which is why it dominates the related
        methods of this class. Therefore a good handle method will sleep for
        some amount of time, then add messages to the outbox
        """
        raise NotImplementedError("Actors must define how they handle messages.")

    def activate(self):
        """
        On activation hydrate the actor to start listening for messages.
        """
        self.active  = True
        self.hydrate.succeed()
        self.hydrate = None

    def deactivate(self):
        """
        On deactivation, dehydrate the actor to stop listening for messages.
        """
        self.active  = False
        self.hydrate = self.env.event()
        yield self.hydrate

    def listen(self):
        """
        Listen for an incomming message
        """
        self.ready = True
        self.message = self.env.event()
        yield self.message

    def is_listening(self):
        """
        Returns True if the actor is listening for a message, else False.
        """
        return self.ready and self.message is not None

    def persist(self):
        """
        Fixed time cost for writing to the database.
        """
        yield self.env.timeout(PERSISTENCE_COST)

    def send(self, message):
        """
        Sends messages using the actor manager.
        """
        yield self.env.timeout(SEND_LATENCY)
        self.manager.route(message)

    def recv(self, value):
        """
        Called on receipt of a message from the node.
        """
        self.ready = False
        self.message.succeed()
        self.message = None
        self.handle(value)

    def run(self):
        """
        Primary execution loop of the simulated program. This loop essentially
        waits for messages and then handles them when they occur.
        """

        while True:

            if not self.active:
                # Await the hydration event
                yield self.env.process(self.deactivate())

            else:
                # Listen for a message
                yield self.env.process(self.listen())

                # Process the messages in the outbox
                for msg in self.outbox:
                    yield self.env.process(self.send(msg))

                # If we must persist then do so
                if self.checkpoint:
                    yield self.env.process(self.persist())
