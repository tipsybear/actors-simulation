# gvas.cluster.base
# Base classes for cluster simulation framework.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:49:32 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: base.py [] allen.leis@gmail.com $

"""
Base classes for cluster simulation framework.
"""

##########################################################################
# Imports
##########################################################################

from gvas.base import NamedProcess

##########################################################################
# Classes
##########################################################################

class Machine(NamedProcess):

    def __init__(self, env, **kwargs):
        """
        Pass-through for NamedProcess init without keywords
        """
        super(Machine, self).__init__(env)

    @classmethod
    def create(cls, env, *args, **kwargs):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        while True:
            yield cls(env, *args, **kwargs)

    def send(self, *args, **kwargs):
        """
        Generalized method to put message onto the contained network.
        """
        raise NotImplementedError('Subclasses should override this method.')

    def recv(self, *args, **kwargs):
        """
        Generalized method to obtain a message from the contained network.
        """
        raise NotImplementedError('Subclasses should override this method.')
