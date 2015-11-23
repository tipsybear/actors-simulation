# tests.test_dynamo
# Tests for the dynamo sequence generators and utilities.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Mon Nov 23 17:11:41 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: tests.test_dynamo.py [] benjamin@bengfort.com $

"""
Tests for the dynamo sequence generators and utilities.
"""

##########################################################################
## Imports
##########################################################################

import unittest

from gvas.dynamo import Sequence
from gvas.dynamo import ExponentialSequence
from gvas.dynamo import NormalDistribution

##########################################################################
## Sequence Tests
##########################################################################

class SequenceTests(unittest.TestCase):
    """
    Make sure that the sequences behave as expected.
    """

    def test_unit_sequence(self):
        """
        Ensure an "infinite" sequence works as expected.
        """
        sequence = Sequence()
        for idx in xrange(1, 100000):
            self.assertEqual(sequence.next(), idx)

    def test_step_sequence(self):
        """
        Ensure that a stepped sequence works as expected.
        """
        sequence = Sequence(step=10)
        for idx in xrange(10, 100000, 10):
            self.assertEqual(sequence.next(), idx)

    def test_limit_sequence(self):
        """
        Ensure that a sequence can be limited.
        """
        with self.assertRaises(StopIteration):
            sequence = Sequence(limit=1000)
            for idx in xrange(1, 100000):
                self.assertEqual(sequence.next(), idx)

    def test_exponential_unit_sequence(self):
        """
        Ensure an "infinite" exponential sequence works as expected.
        """
        sequence = ExponentialSequence()
        for idx in xrange(1, 1000):
            self.assertEqual(sequence.next(), 2**idx)

    def test_exponential_base_sequence(self):
        """
        Ensure that an exponential sequence with a different base works.
        """
        sequence = ExponentialSequence(base=10)
        for idx in xrange(1, 1000):
            self.assertEqual(sequence.next(), 10**idx)

    def test_exponential_limit_sequence(self):
        """
        Ensure that a sequence can be limited.
        """
        with self.assertRaises(StopIteration):
            sequence = ExponentialSequence(limit=1000)
            for idx in xrange(1, 100000):
                self.assertEqual(sequence.next(), 2**idx)


##########################################################################
## Distribution Tests
##########################################################################

class DistributionTests(unittest.TestCase):
    """
    Make sure that the distributions behave as expected.
    """

    def test_normal(self):
        """
        Weak test of normal distributions.
        """
        standard = NormalDistribution(0, 1)
        for idx in xrange(100000):
            event = standard.next()
            self.assertGreater(event, -5)
            self.assertLess(event, 5)

    def test_normal_mean(self):
        """
        Assert that the mean approximates the distribution.
        """
        dist    = NormalDistribution(0, 1)
        samples = 1000000
        total   = sum(dist.next() for idx in xrange(samples))
        mean    = total / samples

        self.assertAlmostEqual(mean, 0.0, places=3)
