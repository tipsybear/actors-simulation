# gvas.exceptions
# Exception hierarchy for gvas simulations
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Mon Nov 23 16:42:33 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: exceptions.py [] benjamin@bengfort.com $

"""
Exception hierarchy for gvas simulations
"""

##########################################################################
## Exception Hierarchy
##########################################################################

class GVASException(Exception):
    """
    The root exception for any actor simulations.
    """
    pass

class UnknownType(GVASException):
    """
    An unknown type was passed causing a TypeError of some kind.
    """
    pass

##########################################################################
## Console Exceptions
##########################################################################

class ConsoleError(GVASException):
    """
    Errors that occur from user input on the GVAS console utility
    """
    pass
