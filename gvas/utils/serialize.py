# gvas.utils.serialize
# Provides helpers for JSON and CSV serialization to disk.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Dec 06 21:37:53 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: gvas.utils.serialize.py [] benjamin@bengfort.com $

"""
Provides helpers for JSON and CSV serialization to disk.
"""

##########################################################################
## Imports
##########################################################################

import json

from gvas.utils.timez import dthandler

##########################################################################
## JSON encoding
##########################################################################

class JSONEncoder(json.JSONEncoder):

    def encode_datetime(self, obj):
        """
        Converts a datetime object into epoch time.
        """
        return dthandler(obj)

    def encode_ndarray(self, obj):
        """
        Convert np.array to a list object.
        """
        return list(obj)

    def default(self, obj):
        """
        Perform encoding of complex objects.
        """
        try:
            return super(JSONEncoder, self).default(obj)
        except TypeError:
            # If object has a serialize method, return that.
            if hasattr(obj, 'serialize'):
                return obj.serialize()

            # Look for an encoding method on the Encoder
            method = "encode_%s" % obj.__class__.__name__
            if hasattr(self, method):
                method = getattr(self, method)
                return method(obj)

            # Not sure what is going on if the above two methods didn't work
            raise TypeError(
                "Could not encode type '{0}' using {1}\n"
                "Either add a serialze method to the object, or add an "
                "encode_{0} method to {1}".format(
                    obj.__class__.__name__, self.__class__.__name__
                )
            )
