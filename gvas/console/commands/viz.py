# gvas.console.commands.viz
# Accepts an results json file and outputs a png of the timeseries.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Mon Dec 07 23:33:23 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: viz.py [] benjamin@bengfort.com $

"""
Accepts an results json file and outputs a png of the timeseries.
"""

##########################################################################
## Imports
##########################################################################

import os
import re
import argparse
import unicodedata

from gvas.results import Results
from gvas.console.commands.base import Command


##########################################################################
# Helper Functions
##########################################################################

def slugify(text):
    slug = unicodedata.normalize("NFKD",unicode(text)).encode("ascii", "ignore")
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    return slug

##########################################################################
# Command
##########################################################################

class VizCommand(Command):

    name = "viz"
    help = "create a visualization of the timeseries in a results file."

    args = {
        ('-o', '--output'): {
            'type': str,
            'default': '.',
            'metavar': 'DIR',
            'help': 'specify directory to write the image(s) to'
        },
        'results': {
            'nargs': '+',
            'type': argparse.FileType('r'),
            'help': 'the path to the results file to visualize',
        },
    }

    def handle(self, args):
        """
        Handle command line arguments
        """

        output = []

        for result in args.results:
            output.append(self.handle_result(result, args))

        return "\n".join(output)

    def handle_result(self, fp, args):
        """
        Handle individual results.
        """

        # Load the results
        result = Results.load(fp)

        # Compute the image path
        path = os.path.join(
            args.output,
            "{}-{}.png".format(
                slugify(result.simulation),
                result.get_finished().strftime("%Y%m%d")
            )
        )

        # Write the image to disk
        plot = result.plot()
        plot.get_figure().savefig(path)


        return "Saved {} to {}".format(result.get_title(), path)
