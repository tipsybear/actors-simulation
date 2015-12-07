# gvas.dynamo
# These utilities are "generators" e.g. classes that produce things.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Mon Nov 23 16:46:34 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: dynamo.py [] benjamin@bengfort.com $

"""
These utilities are "generators" e.g. classes that produce things. These are
the essential tools for generating events in the system particularly random
events or other sequences that we will use in our processes.
"""

##########################################################################
## Imports
##########################################################################

import random

from gvas.viz import plot_kde
from gvas.config import settings
from gvas.exceptions import UnknownType

##########################################################################
## Base Dynamo
##########################################################################


class Dynamo(object):
    """
    A dynamo is a numeric generator for use in our simulation. Right now this
    simply exposes the standard interface for a Python iterator, but may do
    more in the future.
    """

    def next(self):
        raise NotImplementedError("Dynamos must have a next method.")

    def __iter__(self):
        return self

##########################################################################
## Sequences
##########################################################################


class Sequence(Dynamo):
    """
    An infinite sequence and counter object.
    This is a bit more logic than exposed by `itertools.count()`
    Note that unlike xrange, start is never yielded, and the limit is
    inclusive, e.g. the range in a sequence is (start, limit]
    """

    def __init__(self, start=0, limit=None, step=1):
        self.value = start
        self.step  = step
        self.limit = limit

    def next(self):
        self.value += self.step

        if self.limit is not None and self.value > self.limit:
            raise StopIteration("Stepped beyond limit value!")

        return self.value


class ExponentialSequence(Sequence):
    """
    An infinite exponential sequence (for funsies).
    """

    def __init__(self, start=0, base=2, limit=None):
        self.base  = base
        self.power = start
        self.limit = limit

    @property
    def value(self):
        return self.base ** self.power

    def next(self):
        self.power += 1

        if self.limit is not None and self.value > self.limit:
            raise StopIteration("Exponential ceiling reached!")

        return self.value

##########################################################################
## Distributions
##########################################################################


class Distribution(Dynamo):
    """
    A Distribution is a Dynamo (an iterator that generates numbers) but
    because it models random samples, a `get` method is aliased to `next`.
    """

    def get(self):
        return self.next()

    def plot(self, n=100, **kwargs):
        """
        Vizualizes the density estimate of the distribution.
        """
        random.seed(kwargs.get('random_seed', settings.random_seed))
        series = [self.get() for x in xrange(n)]
        axe = plot_kde(series, **kwargs)

        axe.set_ylabel('frequency')
        axe.set_xlabel('value')
        axe.set_title(
            '{} Distribution Plot'.format(
            self.__class__.__name__.rstrip('Distribution')
        ))
        
        return axe


class UniformDistribution(Distribution):
    """
    Generates uniformly distributed values inside of a range. Basically a
    wrapper around `random.randint` and `random.uniform` depending on type.
    """

    def __init__(self, minval, maxval, dtype=None):
        # Detect type from minval and maxval
        if dtype is None:
            if isinstance(minval, int) and isinstance(maxval, int):
                dtype = 'int'
            elif isinstance(minval, float) and isinstance(maxval, float):
                dtype = 'float'
            else:
                raise UnknownType(
                    "Could not detect type from range {!r} to {!r}"
                    .format(minval, maxval)
                )

        # If dtype is given, validate it from given choices.
        if dtype not in {'int', 'float'}:
            raise UnknownType(
                "{!r} is not a valid type, use int or float".format(dtype)
            )

        self.range = (minval, maxval)
        self.dtype = dtype

    def next(self):
        jump = {
            'int': random.randint,
            'float': random.uniform,
        }

        return jump[self.dtype](*self.range)


## Alias for Uniform Distribution
Uniform = UniformDistribution


class NormalDistribution(Distribution):
    """
    Generates normally distributed values
    """

    def __init__(self, mean, stddev):
        self.mean  = mean
        self.sigma = stddev

    def next(self):
        return random.gauss(self.mean, self.sigma)


## Alias for Normal Distribution
Normal = NormalDistribution
