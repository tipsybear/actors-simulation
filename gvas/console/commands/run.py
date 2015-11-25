# gvas.console.commands.run
# Executes a GVAS simulation.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Tue Nov 24 17:40:30 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: run.py [] allen.leis@gmail.com $

"""
Executes a GVAS simulation.
"""

##########################################################################
## Imports
##########################################################################

import sys
import argparse
import colorama

from gvas.console.utils import color_format
from gvas.console.commands.base import Command
from gvas.sims import registry
from gvas.exceptions import UnknownSimulation
from gvas.utils.decorators import Timer

##########################################################################
## Command
##########################################################################

class RunCommand(Command):

    name = "run"
    help = "executes a given simulation"

    args = {
        ('-v', '--verbose'): {
            'action': 'count',
            'default': 1,
            'help': 'set the verbosity of the command',
        },
        ('-o', '--output'): {
            'type': argparse.FileType('w'),
            'default': sys.stdout,
            'metavar': 'PATH',
            'help': 'specify location to write output to'
        },
        'name': {
            'nargs': '+',
            'type': str,
            'help': 'the simulation to execute',
        },
    }

    def handle(self, args):
        """
        Handle command line arguments
        """
        # redirect output as requested
        sys.stdout = args.output

        # determine requested simulation
        sname = args.name[0]

        # verify we have a valid simulation
        if sname not in registry:
            raise UnknownSimulation('"{}" is not a valid simulation.'.format(sname))

        # instantiate requested simulation
        simulation = registry[sname].klass()

        # execute simulation and return results
        with Timer() as timer:
            simulation.run()

        # return execution info
        if args.verbose > 0:
            return color_format(
                '"{}" simulation completed in: {}',
                colorama.Fore.CYAN,
                sname,
                timer
            )

        return ""
