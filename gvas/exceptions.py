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


class UnknownSimulation(GVASException):
    """
    The name of an unknown simulation was passed.
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


##########################################################################
## Cluster Resource Exceptions
##########################################################################

class ClusterResourceException(GVASException):
    """
    Base exception for cluster objects
    """
    pass


class ClusterLacksCapacity(ClusterResourceException):
    """
    An error condition wherein a Cluster cannot accept a Node due to the
    lack of available space (all racks are full).
    """
    pass


class NodeLacksCapacity(ClusterResourceException):
    """
    An error condition wherein a Node cannot accept a Program due to the
    lack of available resources (cpu, memory, etc.).
    """
    pass


class RackLacksCapacity(ClusterResourceException):
    """
    An error condition wherein a Rack cannot accept a Node due to the
    lack of available space.
    """
    pass


##########################################################################
## Network Exceptions
##########################################################################

class NetworkException(ClusterResourceException):
    """
    Handling exceptions that occur when trying to send messages.
    """
    pass

class BandwidthExceeded(NetworkException):
    """
    A `Network` resource has exceeded its capacity.
    """
    pass

class UndeliverableMessage(NetworkException):
    """
    A message has arrived at a node that cannot be delivered. 
    """
    pass
