# gvas.cluster.program
# Simulation class to model a program run within a Node instance.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:52:45 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: program.py [] allen.leis@gmail.com $

"""
Simulation class to model a program run within a Node instance.
"""

##########################################################################
# Imports
##########################################################################

from gvas.config import settings
from gvas.base import NamedProcess

##########################################################################
# Classes
##########################################################################

class Program(NamedProcess):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def create(self):
        """
        Generalized factory method to return a generator that can produce
        new instances.
        """
        pass

    def run(self):
        """
        Kicks off execution of a simulated program. This method contains a loop
        to cycle through specific behaviors such as:
            - wait for recv
            - sleep for random time
            - does a send to one or more other Programs/Nodes
            - repeat
        """
        pass

    @property
    def ports(self):
        """
        A list of port numbers this program uses.
        """
        pass


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
