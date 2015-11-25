# gvas.sims
# A package of discrete simulations that use the Actor model.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Nov 22 11:56:48 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
A package of discrete simulations that use the Actor model.
"""

##########################################################################
## Imports
##########################################################################

from collections import namedtuple

from .cars import GasStationSimulation

##########################################################################
## Classes
##########################################################################

Simulation = namedtuple('Simulation', 'name description klass')

##########################################################################
## Module Variables
##########################################################################

registry = {
    'cars': Simulation(
        'cars',
        'The tutorial simulation from SimPy to frame running simulations.',
        GasStationSimulation
    ),
}
