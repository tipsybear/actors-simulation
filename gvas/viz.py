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
