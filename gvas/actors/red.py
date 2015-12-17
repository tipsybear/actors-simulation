# gvas.actors.red
# The red actor programs for simulating actor behavor on the cluster.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Thu Dec 17 01:37:35 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: red.py [] allen.leis@gmail.com $

"""
The red actor programs for simulating actor behavor on the cluster.
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

class RedActor(ActorProgram):
    """
    the first actors sends four messages, teh second actor type sends two,a nd the third sends three
    """

    colors = ['red', 'magenta', 'crimson', 'apple']

    def __init__(self, *args, **kwargs):
        self.color = self.colors[0]
        super(RedActor, self).__init__(*args, **kwargs)

    def next_color(self):
        """
        finds next color in the cycle
        """
        index = self.colors.index(self.color)
        if index >= len(self.colors) - 1:
            return None
        else:
            return self.colors[index + 1]

    def _handle_red(self, message):
        for i in range(4):
            msg = Message(None, None, 1, MESSAGE_SIZE, self.env.now, 'magenta')
            self.outbox.append(msg)

    def _handle_magenta(self, message):
        for i in range(2):
            msg = Message(None, None, 1, MESSAGE_SIZE, self.env.now, 'crimson')
            self.outbox.append(msg)

    def _handle_crimson(self, message):
        for i in range(3):
            msg = Message(None, None, 1, MESSAGE_SIZE, self.env.now, 'apple')
            self.outbox.append(msg)

    def _handle_apple(self, message):
        pass

    def handle(self, message):
        self.logger.info("ACTOR: ID: {}, WORKING ({})".format(self.id, message.color))
        yield self.env.timeout(0)

        color = message.color

        if color == 'red':
            self._handle_red(message)
        elif color == 'magenta':
            self._handle_magenta(message)
        elif color == 'crimson':
            self._handle_crimson(message)
        else:
            self._handle_apple(message)
