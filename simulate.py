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

from gvas.console import GVASUtility

##########################################################################
## Main method
##########################################################################

if __name__ == '__main__':
    utility = GVASUtility.load()
    utility.execute()
