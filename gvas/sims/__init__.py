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
from .simple import SimpleSimulation
from .balance import BalanceSimulation
from .communications import CommunicationsSimulation

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
    'simple': Simulation(
        'simple',
        'A straightforward simulation to test the Cluster framework.',
        SimpleSimulation
    ),
    'balance': Simulation(
        'balance',
        'A load balancing simulation with the actor model.',
        BalanceSimulation
    ),
    'communications': Simulation(
        'communications',
        'A simulation that can model different communication patterns.',
        BalanceSimulation
    )
}
