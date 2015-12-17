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

# from gvas.cluster import Program
# from gvas.config import settings
# from gvas.utils.logger import LoggingMixin
from .base import ActorProgram

##########################################################################
## Actor Programs
##########################################################################

# blue, teal, cyan, navy, and sky

class BlueActor(ActorProgram):

    colors = ['blue', 'teal', 'cyan', 'navy', 'sky']

    def __init__(self, *args, **kwargs):
        self.color = 'blue'
        super(BlueActor, self).__init__(*args, **kwargs)


    def handle(self, message):
        self.logger.info("ACTOR: ID: {}, WORKING".format(self.id))
        yield self.env.timeout(1)

        # add to outbox
