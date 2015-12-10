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
        super(ActorManager, self).__init__(env)

    def run(self):
        """
        Since this is a process it has to run.
        """
        yield self.env.timeout(1)
