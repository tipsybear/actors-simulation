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
from dateutil import rrule
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


def weekday_before(weekday='Sunday', day=None, weekbuff=None):
    """
    Returns the datetime of the weekday before the specified date, or if None,
    the weekday before today. Note, if today is the same as the weekday, it
    returns the date a week ago from today.

    So by default, this returns the datetime of the Sunday before today.

    The weekbuff subtracts days so that the "beginning of the week" can be
    extended by weekbuff number of days into the next week. E.g. if weekbuff
    is 2 then Monday and Tuesday will find the week before the previous Sunday.

    TODO: Remove the weekbuff when analytics is scheduled.
    """
    offsets = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day     = day or date.today()

    weekbuff = weekbuff if weekbuff is not None else settings.weekbuff
    if weekbuff:
        day = day - timedelta(days=weekbuff)

    offset  = offsets.index(weekday.lower())
    weekday = day - timedelta(days=day.weekday()) + timedelta(days=offset, weeks=-1)

    return datetime(weekday.year, weekday.month, weekday.day)


def groupby_period(series, groupkey, limit=None):
    """
    Expects an ordered timeseries (ordered is important!) of datetimes, and
    returns a generator of groups grouped by the groupkey which should be a
    period identifier like day, week, month, or year.

    If limit is specified, it will stop yielding groups after the specified
    limit of groups has been reached.
    """
    groupkey = {
        'day': lambda dt: dt.isocalendar(),
        'week': lambda dt: dt.isocalendar()[:2],
        'month': lambda dt: (dt.year, dt.month),
        'year': lambda dt: dt.year,
    }[groupkey]

    for idx, (period, grp) in enumerate(groupby(series, key=groupkey)):
        yield period, list(grp)
        if limit and idx+1 >= limit:
            break


def timeperiods(groupkey, start=None, until=None):
    """
    Creates a list of time periods from the given date (default the beginning)
    of the current year) until the specfied date (default today).

    This method essentially wraps the `dateutil.rrule` method with specific
    functionality for dealing with time periods in Smoak.
    """

    until = until or datetime.now()
    start = start or datetime(until.year, 1, 1)

    # group key is interval, converter tuples for use in rrule.
    interval, groupkey = {
        'day': (rrule.DAILY, lambda dt: dt.isocalendar()),
        'week': (rrule.WEEKLY, lambda dt: dt.isocalendar()[:2]),
        'month': (rrule.MONTHLY, lambda dt: (dt.year, dt.month)),
        'year': (rrule.YEARLY, lambda dt: dt.year),
    }[groupkey]

    for period in rrule.rrule(interval, dtstart=start, until=until):
        yield groupkey(period)


def filled_timeperiods(groups, groupkey, **kwargs):
    """
    Fills timeperiods from the `timeperiods` function with groups from the
    `groupby_period` function to get a correct timeseries of grouped data. E.g.
    this fills the group with empty lists where there was a missing period.

    This function is used to generate date range histograms and period groups.

    NOTE: The first date in groups must be less than or equal to the start of
    the timeperiods, which by default is the first of the year. Pass in start
    and until keyword arguments to extend the timeperiods range.

    TODO: Range start and finish detection.
    """

    # Create a filled timeperiod range and initialize fill index.
    dtrange = [(period, []) for period in timeperiods(groupkey, **kwargs)]
    dtindex = 0
    numgrps = len(groups)

    # For every item in our filled range, replace empty lists with groups.
    for idx, (period, empty) in enumerate(dtrange):
        if numgrps > dtindex and period == groups[dtindex][0]:
            yield groups[dtindex]
            dtindex += 1
        else:
            yield period, empty


##########################################################################
## Clock Module
##########################################################################


class Clock(object):
    """
    A time serializer that wraps local and utc time collection and
    maintains knowledge of how to format the times for particular uses.
    Intended usage is as follows:

        >>> clock = Clock("json", local=False) # UTC JSON formatter
        >>> print clock
        2013-11-07T14:35:16.611224Z
        >>> time.sleep(30)
        >>> print clock
        2013-11-07T14:35:46.611661Z

    """

    FORMATS = {
        "long":    HUMAN_DATETIME,
        "json":    JSON_DATETIME,
        "short":   HUMAN_DATE,
        "clock":   HUMAN_TIME,
        "iso8601": ISO8601_DATETIME,
        "iso":     ISO8601_DATETIME,
        "isodate": ISO8601_DATE,
        "isotime": ISO8601_TIME,
        "human":   HUMAN_DATETIME,
        "common":  COMMON_DATETIME,
        "apache":  COMMON_DATETIME,
    }

    @staticmethod
    def localnow():
        return datetime.now(tzlocal())

    @staticmethod
    def utcnow():
        now = datetime.utcnow()
        now = now.replace(tzinfo=tzutc())
        return now

    def __init__(self, default=None, local=False, formats={}):
        default = default or settings.datefmt

        self.formats = self.FORMATS.copy()
        self.formats.update(formats)
        self.default_format = default.lower().replace('-', '').replace('_', '')
        self.use_local = local

    def format(self, dt, fmt=None):
        fmt = fmt or self.default_format
        if fmt in self.formats:
            fmt = self.formats[fmt]
        return dt.strftime(fmt)

    def strfnow(self, fmt=None):
        nowdt  = self.localnow() if self.use_local else self.utcnow()
        return self.format(nowdt, fmt)

    def __str__(self):
        return self.strfnow()

if __name__ == '__main__':
    clock = Clock(local=True)
    print clock
    time.sleep(30)
    print clock
