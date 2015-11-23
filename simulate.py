#!/usr/bin/env python
# simulate
# A command line script that acts as the entry point for simulation.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu Nov 05 15:18:14 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: simulate.py [] benjamin@bengfort.com $

"""
A command line script that acts as the entry point for simulation.
"""

##########################################################################
## Imports
##########################################################################

import gvas
import argparse

from gvas.sims.cars import GasStationSimulation

##########################################################################
## Module Configuration
##########################################################################

DESCRIPTION = "Run an Actor simulation with various parameters"
VERSION     = gvas.get_version()
EPILOG      = "Please file bug reports on Github"

##########################################################################
## Main Method
##########################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION, version=VERSION, epilog=EPILOG)
    args   = parser.parse_args()
    sim    = GasStationSimulation()
    sim.run()
