# test_viz
# Vizualization tests
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Dec 06 20:45:32 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: test_viz.py [] benjamin@bengfort.com $

"""
Vizualization tests
"""

##########################################################################
## Imports
##########################################################################

import unittest
import gvas.viz

from peak.util.imports import lazyModule

##########################################################################
## Vizualization and Configuration Tests
##########################################################################

class VizTests(unittest.TestCase):

    def test_lazyimport(self):
        """
        Test that the viz module is lazily imported.
        """
        
        self.assertEqual(type(gvas.viz.sns), type(lazyModule('seaborn')))
        self.assertEqual(type(gvas.viz.plt), type(lazyModule('matplotlib.pyplot')))
        self.assertEqual(type(gvas.viz.np), type(lazyModule('numpy')))
        self.assertEqual(type(gvas.viz.pd), type(lazyModule('pandas')))
