# gvas.utils.encoding
# str to/from unicode helper functions
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Nov 24 17:35:49 2015 -0500
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: encoding.py [] benjamin@bengfort.com $

"""
str to/from unicode helper functions
"""

##########################################################################
## Encode and Decode utilities
##########################################################################

def encode(value, encoding='utf-8', errors='strict'):
        """
        Converts a unicode object to a str object
        """
        if value is None:
            return ''

        if isinstance(value, basestring):
            if isinstance(value, unicode):
                return value.encode(encoding, errors)
            if isinstance(value, str):
                return value

        raise TypeError(
            "Could not encode this value, must be str or unicode, got {}"
            .format(type(value).__name__)
        )


def decode(value, encoding='utf-8', errors='strict'):
        """
        Converts a str object to a unicode object
        """
        if value is None:
            return u''

        if isinstance(value, basestring):
            if isinstance(value, str):
                return value.decode(encoding, errors)
            if isinstance(value, unicode):
                return value

        raise TypeError(
            "Could not decode this value, must be str or unicode, got {}"
            .format(type(value).__name__)
        )
