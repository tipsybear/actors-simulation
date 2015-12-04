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

import seaborn as sns
import matplotlib.pyplot as plt

from gvas.config import settings

##########################################################################
## Helper Functions
##########################################################################

def configure(**kwargs):
    """
    Sets various configurations for Seaborn from the settings or arguments.
    """

    # Get configurations to do modifications on them.
    style   = kwargs.get('style', settings.vizualization.style)
    context = kwargs.get('style', settings.vizualization.context)
    palette = kwargs.get('style', settings.vizualization.palette)

    # Set the configurations on SNS
    sns.set_style(style)
    sns.set_context(context)
    sns.set_palette(palette)
