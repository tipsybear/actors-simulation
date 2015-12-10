# gvas.viz
# Helper functions for creating output vizualiations from simulations.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Fri Dec 04 13:49:54 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: viz.py [] benjamin@bengfort.com $

"""
Helper functions for creating output vizualiations from simulations.
"""

##########################################################################
## Imports
##########################################################################

from gvas.config import settings
from peak.util.imports import lazyModule

# Perform lazy loading of vizualiation libraries
sns = lazyModule('seaborn')
plt = lazyModule('matplotlib.pyplot')
np  = lazyModule('numpy')
pd  = lazyModule('pandas')

##########################################################################
## Helper Functions
##########################################################################

def configure(**kwargs):
    """
    Sets various configurations for Seaborn from the settings or arguments.
    """

    # Get configurations to do modifications on them.
    style   = kwargs.pop('style', settings.vizualization.style)
    context = kwargs.pop('context', settings.vizualization.context)
    palette = kwargs.pop('palette', settings.vizualization.palette)

    # Set the configurations on SNS
    sns.set_style(style)
    sns.set_context(context)
    sns.set_palette(palette)

    return kwargs


def plot_kde(series, **kwargs):
    """
    Helper function to plot a density estimate of some distribution.
    """
    kwargs = configure(**kwargs)
    return sns.distplot(np.array(series), **kwargs)


def plot_time(series, **kwargs):
    """
    Helper function to plot a simple time series on an axis.
    """
    kwargs = configure(**kwargs)
    return sns.tsplot(np.array(series), **kwargs)


def plot_results(results, **kwargs):
    """
    Sort of a circular plot function so that we can store all vizualization
    related utilities in this package rather than in the results package.
    """
    # Convert data into pandas readable values
    series = np.dstack(results.results.values())
    names  = pd.Series(results.results.keys(), name="results")
    step   = pd.Series(range(0, results.timesteps), name="timestep")

    # Create time series plot
    kwargs = configure(**kwargs)
    axe = sns.tsplot(series, time=step, condition=names, value="value")

    # Configure the graphic
    axe.set_title(results.get_title())

    return axe
