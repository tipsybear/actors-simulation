# gvas.utils.timez
# Time string utilities for ensuring that the timezone is properly handled.
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Tue Nov 24 17:35:49 2015 -0500
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: timez.py [] benjamin@bengfort.com $

"""
Time string utilities for ensuring that the timezone is properly handled.
"""

##########################################################################
## Imports
##########################################################################

import re
import time

from itertools import groupby
from calendar import timegm
from dateutil.tz import tzlocal, tzutc
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser

from gvas.config import settings

##########################################################################
## Format constants
##########################################################################

HUMAN_DATETIME   = "%a %b %d %H:%M:%S %Y %z"
HUMAN_DATE       = "%b %d, %Y"
HUMAN_TIME       = "%I:%M:%S %p"
JSON_DATETIME    = "%Y-%m-%dT%H:%M:%S.%fZ" # Must be UTC
ISO8601_DATETIME = "%Y-%m-%dT%H:%M:%S%z"
ISO8601_DATE     = "%Y-%m-%d"
ISO8601_TIME     = "%H:%M:%S"
COMMON_DATETIME  = "%d/%b/%Y:%H:%M:%S %z"

##########################################################################
## Module helper functions
##########################################################################

zre = re.compile(r'([\-\+]\d{4})')
def strptimez(dtstr, dtfmt):
    """
    Helper function that performs the timezone calculation to correctly
    compute the '%z' format that is not added by default in Python 2.7.
    """
    if '%z' not in dtfmt:
        return datetime.strptime(dtstr, dtfmt)

    dtfmt  = dtfmt.replace('%z', '')
    offset = int(zre.search(dtstr).group(1))
    dtstr  = zre.sub('', dtstr)
    delta  = timedelta(hours = offset/100)
    utctsp = datetime.strptime(dtstr, dtfmt) - delta
    return utctsp.replace(tzinfo=tzutc())


def dthandler(obj, dtftmt="%Y-%m-%dT%H:%M:%S"):
    """
    JSON helper function that provides a handler for Python datetime objects,
    returning the ISO 8601 format.
    """
    dthandler = None
    if isinstance(obj, datetime) or isinstance(obj, date):
       dthandler = obj.strftime(dtftmt)
    return dthandler


def today():
    """
    Returns a datetime for today with hours, minutes, and microseconds
    replaced to zero values (e.g. midnight).
    """
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def epochftime(dt):
    """
    Returns the Unix epoch time from a datetime. The epoch time is the number
    of seconds since January 1, 1970 at midnight UTC.
    """

    # Handle timezone aware datetime objects
    if dt.tzinfo is not None and dt.utcoffset() is not None:
        dt = dt.replace(tzinfo=None) - dt.utcoffset()

    return timegm(dt.timetuple())


def epochptime(epoch):
    """
    Returns a date time from a Unix epoch time.
    """
    if isinstance(epoch, basestring):
        epoch = float(epoch)

    if isinstance(epoch, float):
        epoch = int(epoch)

    return datetime.utcfromtimestamp(epoch).replace(tzinfo=tzutc())


def strpepoch(string):
    """
    Parses a datetime string and returns an epoch time. The datetime string
    can be anything parsable by dateutil.parser or an int or float. May raise
    a ValueError if at any step in the chain, the date string isn't parsable.
    """
    # Step one, attempt to parse the date
    try:
        string = parser.parse(string)
    except ValueError:
        # Could be an integer or float string
        try:
            string = epochptime(string)
        except ValueError:
            pass

    if not isinstance(string, datetime):
        raise ValueError("Couldn't parse '{}' as epoch".format(string))

    return epochftime(string)


def humanizedelta(*args, **kwargs):
    """
    Wrapper around dateutil.relativedelta (same construtor args) and returns
    a humanized string representing the detla in a meaningful way.
    """
    delta = relativedelta(*args, **kwargs)
    attrs = ('years', 'months', 'days', 'hours', 'minutes', 'seconds')
    parts = [
        '%d %s' % (getattr(delta, attr), getattr(delta, attr) > 1 and attr or attr[:-1])
        for attr in attrs if getattr(delta, attr)
    ]

    return " ".join(parts)
