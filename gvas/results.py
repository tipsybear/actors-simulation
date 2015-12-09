# gvas.results
# Manages the serialization of experimental results and their reporting.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Dec 06 21:00:52 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: results.py [] benjamin@bengfort.com $

"""
Manages the serialization of experimental results and their reporting.
"""

##########################################################################
## Imports
##########################################################################

import json
import gvas

from gvas.config import settings
from gvas.viz import plot_results
from gvas.utils.serialize import JSONEncoder
from gvas.utils.decorators import Timer
from gvas.utils.timez import HUMAN_DATETIME
from gvas.utils.timez import epochptime

##########################################################################
## Results Object
##########################################################################

class Results(object):
    """
    A data stucture for managing results data.
    """

    @classmethod
    def load(klass, fp):
        """
        Load a results object from a JSON file on disk.
        """
        data = json.load(fp)
        return klass(**data)

    def __init__(self, **kwargs):
        # Set reasonable defaults for results
        self.results    = {}
        self.timer      = Timer()
        self.simulation = None
        self.version    = gvas.get_version()
        self.randseed   = settings.random_seed
        self.timesteps  = settings.max_sim_time
        self.cluster    = settings.defaults

        # Set any properties that need to be serialized (override above)
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

    def dump(self, fp, **kwargs):
        """
        Write the results object back down to disk.
        """
        kwargs['cls'] = kwargs.get('cls', JSONEncoder)
        json.dump(self, fp, **kwargs)

    def serialize(self):
        """
        Returns an iterator of key, value pairs of writeable properites.
        """

        def properties(self):
            for key, val in self.__dict__.iteritems():
                if not key.startswith('_') and not callable(val):
                    yield (key, val)

        return dict(properties(self))

    def plot(self, **kwargs):
        """
        Alias for gvas.viz.plot_results
        """
        return plot_results(self, **kwargs)

    def get_title(self):
        """
        Returns a pretty title for the results.
        """
        if hasattr(self, 'title'):
            return self.title

        return '{} Simulation on {}'.format(
            self.simulation, self.get_finished().strftime(HUMAN_DATETIME)
        )

    def get_finished(self):
        """
        Returns the finished datetime from the timer.
        """
        finished = self.timer.finished if isinstance(self.timer, Timer) else self.timer['finished']
        return epochptime(finished)
