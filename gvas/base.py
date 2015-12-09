# gvas.base
# The base API for simulation processes and scripts.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Mon Nov 23 17:40:57 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: base.py [] benjamin@bengfort.com $

"""
The base API for simulation processes and scripts.
"""

##########################################################################
## Imports
##########################################################################

import simpy
import random

from datetime import datetime
from gvas.config import settings
from gvas.dynamo import Sequence
from gvas.results import Results
from gvas.utils.logger import LoggingMixin
from gvas.utils.timez import HUMAN_DATETIME

##########################################################################
## Base Process Objects
##########################################################################


class Process(object):
    """
    Base process object.
    """

    def __init__(self, env):
        self.env    = env
        self.action = env.process(self.run())

    def run(self):
        raise NotImplementedError("Processes must implement a run method.")


class NamedProcess(Process):
    """
    A process with a sequence counter and self identification.
    """

    counter = Sequence()

    def __init__(self, env):
        self._id = self.counter.next()
        super(NamedProcess, self).__init__(env)

    @property
    def name(self):
        return "{} #{}".format(self.__class__.__name__, self._id)


##########################################################################
## Base Simulation Script
##########################################################################

class Simulation(LoggingMixin):
    """
    Defines a script that every simulation implements.
    """

    def __init__(self, **kwargs):
        """
        Instantiates the simpy environment and other configurations.
        """
        random.seed(kwargs.get('random_seed', settings.random_seed))

        self.max_sim_time = kwargs.get('max_sim_time', settings.max_sim_time)
        self.env = simpy.Environment()

    @property
    def diary(self):
        """
        Allen has chosen to name the simulation results the diary, this property
        attempts to auto-configure the results object before being loaded.
        """
        if not hasattr(self, '_diary'):
            self._diary = Results(simulation=self.__class__.__name__)
        return self._diary

    def script(self):
        """
        Use the environment to generate a script.
        """
        raise NotImplementedError("Every simulation requires a script.")

    def setup(self):
        """
        Override to do any work before the simulation runs like logging or
        cleaning up output files. Call super to ensure logging works.
        """
        message = (
            "{} Simulation started at {}"
            .format(self.__class__.__name__, datetime.now().strftime(HUMAN_DATETIME))
        )

        self.logger.info(message)

    def complete(self):
        """
        Override for a final report or cleanup at the end of the run.
        Call super to ensure logging works correctly
        """
        message = (
            "{} Simulation finshed at {} ({})"
            .format(self.__class__.__name__, datetime.now().strftime(HUMAN_DATETIME), self.diary.timer)
        )

        self.logger.info(message)

    def run(self):
        """
        The entry point for all simulations.
        """
        # Call setup and initialization function
        self.setup()

        # Time the entire simulation run process.
        with self.diary.timer:

            # Set up the simulation environment and run
            self.script()
            self.env.run(until=self.max_sim_time)

        # Call clean and completion functions
        self.complete()
