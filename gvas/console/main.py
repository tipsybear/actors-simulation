# gvas.console.main
# The main GVAS command line utility program
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Tue Nov 24 16:14:04 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: main.py [] allen.leis@gmail.com $

"""
The main GVAS command program.

This program is the core object that is imported by any command line
script, it defines the definition of the GVAS simulation for use on
systems that need to implement GVAS.
"""

##########################################################################
## Imports
##########################################################################

import colorama

from gvas.console.commands import *
from gvas.console.prog import ConsoleProgram

##########################################################################
## Command Line Variables
##########################################################################

DESCRIPTION = "An administrative utility for the GVAS Simulation"
EPILOG      = "For any bugs or concerns, please use issues on Github"
COMMANDS    = [
    ListCommand,
    RunCommand,
]

##########################################################################
## The GVAS Command line Program
##########################################################################

class GVASUtility(ConsoleProgram):

    description = colorama.Fore.CYAN + DESCRIPTION + colorama.Fore.RESET
    epilog      = colorama.Fore.MAGENTA + EPILOG + colorama.Fore.RESET

    @classmethod
    def load(klass, commands=COMMANDS):
        utility = klass()
        for command in commands:
            utility.register(command)
        return utility
