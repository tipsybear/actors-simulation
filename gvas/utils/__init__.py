# gvas.utilities
# Utilities and helper functions common to the GVAS simulation
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Nov 24 17:35:49 2015 -0500
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Utilities and helper functions common to the GVAS simulation.
"""

##########################################################################
## Imports
##########################################################################

from .encoding import encode, decode

##########################################################################
## Helper Functions
##########################################################################

def truncate(iterable, val=0):
    """
    Truncates a list containing some empty value (e.g. 0) at the beginning
    and returns the remainder of the list. Similar to lstrip for strings,
    except this works generically over any iterable.

    Note: this will cause generators to be iterated upon!
    TODO: Generator safe function
    TODO: add ltruncate, rtruncate, and trucate methods similar to strip.
    """
    for idx, item in enumerate(iterable):
        if item != val:
            break

    return iterable[idx:]


def rename(mapping, origkey, newkey):
    """
    Rename a key in a dictionary or mapping by passing in the data structure,
    the original key, and the new key to be renamed.
    """
    mapping[newkey] = mapping.pop(origkey)
