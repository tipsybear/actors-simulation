# gvas.actors.green
# The blue actor programs for simulating actor behavor on the cluster.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Thu Dec 17 01:37:35 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: green.py [] allen.leis@gmail.com $

"""
The green actor programs for simulating actor behavor on the cluster.
"""

##########################################################################
## Imports
##########################################################################

import random

from gvas.config import settings
from .base import ActorProgram
from gvas.cluster.network import Message

##########################################################################
## Module Constants
##########################################################################

MESSAGE_SIZE            = settings.simulations.communications.message_size

##########################################################################
## Actor Programs
##########################################################################

class GreenActor(ActorProgram):
    """
    a node sends two messages; those two actors then send a fixed number of messages
    to actors of their same type (e.g. 5) then forward those on to three more
    actors of a different type

    RED: in the last one, the first actors sends four messages, teh second actor type sends two,a nd the third sends three
    """

    colors = ['green', 'forest', 'seagreen']

    def __init__(self, *args, **kwargs):
        self.color = self.colors[0]
        super(GreenActor, self).__init__(*args, **kwargs)

    def next_color(self):
        """
        finds next color in the cycle
        """
        index = self.colors.index(self.color)
        if index >= len(self.colors) - 1:
            return None
        else:
            return self.colors[index + 1]

    def _handle_green(self, message):
        for i in range(2):
            msg = Message(self.address, None, 3, MESSAGE_SIZE, self.env.now, 'forest')
            self.outbox.append(msg)

    def _handle_forest(self, message):
        if message.value > 1:
            msg = Message(self.address, None, message.value - 1, MESSAGE_SIZE, self.env.now, 'forest')
            self.outbox.append(msg)
        else:
            msg = Message(self.address, None, 1, MESSAGE_SIZE, self.env.now, 'seagreen')
            self.outbox.append(msg)

    def _handle_seagreen(self, message):
        pass

    def handle(self, message):
        self.logger.debug("ACTOR: ID: {}, WORKING ({})".format(self.id, message.color))
        yield self.env.timeout(0)

        color = message.color

        if color == 'green':
            self._handle_green(message)
        elif color == 'forest':
            self._handle_forest(message)
        else:
            self._handle_seagreen(message)
