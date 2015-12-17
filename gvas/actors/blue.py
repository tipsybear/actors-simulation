# gvas.actors.blue
# The blue actor programs for simulating actor behavor on the cluster.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Thu Dec 17 01:37:35 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: blue.py [] allen.leis@gmail.com $

"""
The blue actor programs for simulating actor behavor on the cluster.
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

class BlueActor(ActorProgram):
    """
have one actor create three messages;
but send them on "based on the value"; which for now, could be randomly send to one, send to two, or send to all three
then those do the same thing to the next color
maybe go in three-four colors
    """

    colors = ['blue', 'teal', 'cyan']

    def __init__(self, *args, **kwargs):
        self.color = 'blue'
        super(BlueActor, self).__init__(*args, **kwargs)

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
