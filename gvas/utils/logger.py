# gvas.utils.logger
# Wraps the python logging module for simulation-specific logging.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Dec 09 13:10:59 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: logger.py [] benjamin@bengfort.com $

"""
Wraps the python logging module for simulation-specific logging.
"""

##########################################################################
## Imports
##########################################################################

import getpass
import logging
import colorama
import warnings
import logging.config

from gvas.config import settings
from gvas.dynamo import Sequence

##########################################################################
## Logging configuration: must be run at the module level first
##########################################################################

configuration = {
    'version': 1,
    'disable_existing_loggers': settings.logging.disable_existing_loggers,

    'formatters': {
        'simple': {
            'format':  settings.logging.logfmt,
            'datefmt': settings.logging.datefmt,
        },
    },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },

    'loggers':  {
        'gvas': {
            'level': settings.logging.level,
            'handlers': ['console',],
            'propagagte': True,
        },
        'py.warnings': {
            'level': 'DEBUG',
            'handlers': ['console',],
            'propagate': True,
        },
    },
}

logging.config.dictConfigClass(configuration).configure()
if not settings.debug: logging.captureWarnings(True)

##########################################################################
## Logger utility
##########################################################################

class WrappedLogger(object):
    """
    Wraps the Python logging module's logger object to ensure that all simulation
    logging happens with the correct configuration as well as any extra
    information that might be required by the log file (for example, the user
    on the machine, hostname, IP address lookup, etc).

    Subclasses must specify their logger as a class variable so all instances
    have access to the same logging object.
    """

    logger = None

    def __init__(self, **kwargs):
        self.raise_warnings = kwargs.pop('raise_warnings', settings.debug)
        self.logger = kwargs.pop('logger', self.logger)

        if not self.logger or not hasattr(self.logger, 'log'):
            raise TypeError(
                "Subclasses must specify a logger, not {}"
                .format(type(self.logger))
            )

        self.extras = kwargs

    def log(self, level, message, *args, **kwargs):
        """
        This is the primary method to override to ensure logging with extra
        options gets correctly specified.
        """
        extra = self.extras.copy()
        extra.update(kwargs.pop('extra', {}))

        kwargs['extra'] = extra
        self.logger.log(level, message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        return self.log(logging.DEBUG, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        return self.log(logging.INFO, message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """
        Specialized warnings system. If a warning subclass is passed into
        the keyword arguments and raise_warnings is True - the warnning will
        be passed to the warnings module.
        """
        warncls = kwargs.pop('warning', None)
        if warncls and self.raise_warnings:
            warnings.warn(message, warncls)

        return self.log(logging.WARNING, message, *args, **kwargs)

    # Alias warn to warning
    warn = warning

    def error(self, message, *args, **kwargs):
        return self.log(logging.ERROR, message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        return self.log(logging.CRITICAL, message, *args, **kwargs)

##########################################################################
## The primary Simulation Logger class
##########################################################################

class SimulationLogger(WrappedLogger):
    """
    Usage:
        >>> from gvas.utils.logger import SimulationLogger
        >>> logger = SimulationLogger()
        >>> logger.info("You were here!")

    This will correctly log to the simulation logging handlers and also
    provide the log message id as well as the user running the simulation.
    """

    counter = Sequence()
    logger  = logging.getLogger('gvas')

    def __init__(self, **kwargs):
        self._user = kwargs.pop('user', None)
        super(SimulationLogger, self).__init__(**kwargs)

    @property
    def user(self):
        if not self._user:
            self._user = getpass.getuser()
        return self._user

    def log(self, level, message, *args, **kwargs):
        """
        Provide current user as extra context to the logger
        """
        extra = kwargs.pop('extra', {})
        extra.update({
            'user':  self.user,
            'msgid': self.counter.next(),
        })

        kwargs['extra'] = extra
        super(SimulationLogger, self).log(level, message, *args, **kwargs)


##########################################################################
## Logging Mixin
##########################################################################

class LoggingMixin(object):
    """
    Mix in to classes that need their own logging object!
    """

    @property
    def logger(self):
        """
        Instantiates and returns a SmoakLogger instance
        """
        if not hasattr(self, '_logger') or not self._logger:
            self._logger = SimulationLogger()
        return self._logger

if __name__ == '__main__':
    import random

    loggera = SimulationLogger()
    loggerb = SimulationLogger()

    for idx in xrange(12):
        level  = random.choice([logging.DEBUG, logging.INFO, logging.CRITICAL, logging.WARNING, logging.ERROR])
        name, logger = random.choice([('a', loggera), ('b', loggerb)])

        logger.log(level, "Message from {}".format(name))
