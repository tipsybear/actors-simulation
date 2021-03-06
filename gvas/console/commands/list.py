# gvas.console.commands.list
# List the available GVAS simulations that can be initiated.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Tue Nov 24 16:14:04 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: list.py [] allen.leis@gmail.com $

"""
List the available GVAS simulations that can be initiated.
"""

##########################################################################
# Imports
##########################################################################

from gvas.console.commands.base import Command
from gvas.sims import registry

##########################################################################
# Command
##########################################################################

class ListCommand(Command):

    name = "list"
    help = "enumerate the simulations available for execution"

    args = {
    }

    def handle(self, args):
        """
        Handle command line arguments
        """
        sims = ['\t{}: {}'.format(s.name, s.description)
                for s in registry.itervalues()]

        output = '\n'.join([
            'Available simulations:\n',
            '\n'.join(sims),
            ''
        ])
        return output
