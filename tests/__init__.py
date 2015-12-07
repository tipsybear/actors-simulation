# tests
# Testing for the GVAS simulation
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Nov 03 17:05:07 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: __init__.py [] benjamin@bengfort.com $

"""
Testing for the GVAS simulation
"""

##########################################################################
## Imports
##########################################################################

import unittest

##########################################################################
## Module Constants
##########################################################################

TEST_VERSION = "0.2" ## Also the expected version onf the package

##########################################################################
## Test Cases
##########################################################################

class InitializationTest(unittest.TestCase):

    def test_initialization(self):
        """
        Tests a simple world fact by asserting that 10*10 is 100.
        """
        self.assertEqual(2**3, 8)

    def test_import(self):
        """
        Can import gvas
        """
        try:
            import gvas
        except ImportError:
            self.fail("Unable to import the gvas module!")

    def test_version(self):
        """
        Assert that the version is sane
        """
        import gvas
        self.assertEqual(TEST_VERSION, gvas.__version__)
