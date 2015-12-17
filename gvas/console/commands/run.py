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

##########################################################################
## Command
##########################################################################

class RunCommand(Command):

    name = "run"
    help = "executes a given simulation"

    args = {
        ('-o', '--output'): {
            'type': argparse.FileType('w'),
            'default': None,
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
        # determine requested simulation
        sname = args.name[0]

        # verify we have a valid simulation
        if sname not in registry:
            raise UnknownSimulation('"{}" is not a valid simulation.'.format(sname))

        # instantiate requested simulation
        simulation = registry[sname].klass()
        simulation.run()

        # Dump the output data to a file.
        if args.output is None:
            path = "{}-{}.json".format(sname, simulation.diary.get_finished().strftime("%Y%m%d"))
            args.output = open(path, 'w')
        simulation.diary.dump(args.output)


        return "Results for {} simulation written to {}".format(sname, args.output.name)
