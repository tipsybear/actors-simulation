# gvas.console.prog
# Implements a complete console program.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Nov 24 17:35:49 2015 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: prog.py [] benjamin@bengfort.com $

"""
Implements a complete console program. (Reused from Ben's older code)
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import yaml
import colorama
import argparse
import traceback

from gvas.exceptions import ConsoleError
from gvas.version import get_version
from gvas.config import settings

##########################################################################
## Helper functions
##########################################################################

def handle_default_args(args):
    """
    Include handling of any default arguments that all commands should
    implement here (for example, specifying the pythonpath).
    """

    if hasattr(args, 'pythonpath'):
        if args.pythonpath:
            sys.path.insert(0, args.pythonpath)

    if hasattr(args, 'configpath'):
        if args.configpath and os.path.exists(args.configpath):
            with open(args.configpath, 'r') as conf:
                settings.configure(yaml.load(conf))

##########################################################################
## Console Program
##########################################################################

class ConsoleProgram(object):
    """
    The base program from which all console commands are derived.
    """

    description = None
    epilog      = None
    version     = get_version()

    def __init__(self, **kwargs):
        self.version     = kwargs.get('version', self.__class__.version)
        self.description = kwargs.get('description', self.__class__.description)
        self.epilog      = kwargs.get('epilog', self.__class__.epilog)
        self.commands    = {} # Stores the subcommands of the program

        self._parser     = None
        self._subparsers = None

        ## Init colors
        colorama.init(autoreset=True)

    @property
    def parser(self):
        """
        Instantiates the argparse parser
        """
        if self._parser is None:
            apkw = {
                'description': self.description,
                'epilog':      self.epilog,
                'version':     self.version,
            }
            self._parser = argparse.ArgumentParser(**apkw)
        return self._parser

    @property
    def subparsers(self):
        """
        Insantiates the subparsers for all commands
        """
        if self._subparsers is None:
            apkw = {
                'title': 'commands',
                'description': 'Commands for the %s program' % self.parser.prog,
            }
            self._subparsers = self.parser.add_subparsers(**apkw)
        return self._subparsers

    def register(self, command):
        """
        Registers a command with the program
        """
        command = command()
        if command.name in self.commands:
            raise ConsoleError("Command %s already registered!" % command.name)

        command.create_parser(self.subparsers)
        self.commands[command.name] = command

    def exit(self, code=0, message=None):
        """
        Exit the console program sanely.
        """

        ## If we have a parser, use it to exit
        if self._parser:
            if code > 0:
                self.parser.error(message)
            else:
                self.parser.exit(code, message)

        ## Else we are exiting before parser creation
        else:
            if message is not None:
                if code > 0:
                    sys.stderr.write(message)
                else:
                    sys.stdout.write(message)
            sys.exit(code)

        ## If we're here we didn't exit for some reason?
        raise Exception("Unable to exit the %s" % self.__class__.__name__)

    def execute(self):
        """
        Entry point to the execution of the program.
        """

        # Handle input from the command line
        args = self.parser.parse_args()                # Parse the arguments

        try:
            if not hasattr(args, 'func'):
                raise ConsoleError("No commands registered with this program!")

            handle_default_args(args)                  # Handle the default args
            msg = "%s\n" % args.func(args)             # Call the default function
            self.exit(0, msg)                          # Exit cleanly with message

        except Exception as e:
            if hasattr(args, 'traceback') and args.traceback:
                traceback.print_exc()
            msg = colorama.Fore.RED + str(e)
            self.exit(1, msg)                           # Exit with error

if __name__ == '__main__':
    print get_version()
