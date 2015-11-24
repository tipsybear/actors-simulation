# gvas.console.base
# Base API for all commands in GVAS
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Nov 24 17:35:49 2015 -0500
#
# Copyright (C) 2013 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
Base command to subclass for more specific commands. (Reused Ben's old code).
"""

##########################################################################
## Imports
##########################################################################

import argparse

##########################################################################
## Default Arguments Parser
##########################################################################

class DefaultParser(argparse.ArgumentParser):

    TRACEBACK  = {
        'action':  'store_true',
        'default': False,
        'help': 'On error, show the Python traceback',
    }

    PYTHONPATH = {
        'type': str,
        'required': False,
        'metavar': 'PATH',
        'help': 'A directory to add to the Python path',
    }

    CONFIGPATH = {
        'type': str,
        'required': False,
        'metavar': 'CONF',
        'help': 'Location of YAML configuration file',
    }

    def __init__(self, *args, **kwargs):
        ## Create the parser
        kwargs['add_help'] = False
        super(DefaultParser, self).__init__(*args, **kwargs)

        ## Add the defaults
        self.add_default_arguments()

    def add_default_arguments(self):
        self.add_argument('--traceback', **self.TRACEBACK)
        self.add_argument('--pythonpath', **self.PYTHONPATH)
        self.add_argument('--configpath', **self.CONFIGPATH)

##########################################################################
## Base Command
##########################################################################

class Command(object):
    """
    Provides the base functionality for all commands.
    """

    name    = None
    help    = None
    args    = {}
    parents = [DefaultParser()]

    def __init__(self, **kwargs):
        """
        Initialize the command.
        """
        self.name    = kwargs.get('name', self.__class__.name)
        self.help    = kwargs.get('help', self.__class__.help)
        self.args    = kwargs.get('args', self.__class__.args)
        self.parents = kwargs.get('parents', self.__class__.parents)
        self.parser  = None

    def create_parser(self, subparsers):
        """
        Creates the subparser for this particular command
        """
        self.parser = subparsers.add_parser(self.name, help=self.help, parents=self.parents)
        self.add_arguments()
        self.parser.set_defaults(func=self.handle)
        return self.parser

    def add_arguments(self):
        """
        Definition and addition of all arguments.
        """
        if self.parser is None:
            raise TypeError("Parser cannot be None, has create_parser been called?")

        for keys, kwargs in self.args.items():
            if not isinstance(keys, tuple):
                keys = (keys,)
            self.parser.add_argument(*keys, **kwargs)

    def handle(self, args):
        """
        This is the main entry point to the command helper function, and
        will be passed the arguments that are parsed from the command line
        using argparse.
        """
        raise NotImplementedError("Console utilies should implement.")
