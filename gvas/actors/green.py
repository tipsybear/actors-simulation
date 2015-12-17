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

# blue, teal, cyan, navy, and sky

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

    def handle(self, message):
        self.logger.info("ACTOR: ID: {}, WORKING ({})".format(self.id, message.color))
        yield self.env.timeout(0)

        # add to outbox
        color = self.next_color()
        if color:
            for i in range(random.randint(0, 2)):
                msg = Message(None, None, 1, MESSAGE_SIZE, self.env.now, color)
                self.outbox.append(msg)
