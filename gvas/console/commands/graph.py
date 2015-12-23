# gvas.console.commands.graph
# Parses GraphML output and visualizes it.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Wed Dec 23 15:28:38 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: graph.py [] benjamin@bengfort.com $

"""
Parses GraphML output and visualizes it.
"""

##########################################################################
## Imports
##########################################################################

import os
import networkx as nx

from collections import Counter
from gvas.exceptions import ConsoleError
from gvas.console.commands.base import Command

##########################################################################
## Color Map
##########################################################################

COLORS = {
    # Blue Actor Colors
    'blue': '#1c86ee',
    'teal': '#4a708b',
    'cyan': '#00eeee',

    # Green Actor Colors
    'green': '#00cd00',
    'forest': '#228b22',
    'seagreen': '#54ff9f',

    # Red Actor Colors
    'red': '#ff3030',
    'magenta': '#ee00ee',
    'crimson': '#cd3700',
    'apple': '#ff4500',
}

##########################################################################
## Command
##########################################################################

class GraphCommand(Command):

    name = "graph"
    help = "Postprocesses GraphML file in preparation for visualization."

    args = {
        ('-o', '--output'): {
            'type': str,
            'default': None,
            'metavar': 'PATH',
            'help': 'specify location to write output to'
        },
        'graphml': {
            'nargs': 1,
            'type': str,
            'help': 'the graphml to process',
        },
    }

    def parse_path(self, path):
        """
        Parse path and append modified suffix.
        """
        directory = os.path.dirname(path)
        name, ext = os.path.splitext(os.path.basename(path))

        return os.path.join(directory, "{}-gephi{}".format(name, ext))

    def handle(self, args):
        """
        Handle command line arguments
        """
        path  = args.graphml[0]
        graph = nx.read_graphml(path)

        # Compute the primary color of nodes
        for src in graph.nodes():

            # Counters to modify the source
            count  = 0
            colors = Counter()

            # Iterate through all edges for this source
            for dst in graph[src]:
                edge   = graph[src][dst]
                count += edge['count']

                edge_colors = Counter()
                for color in edge['color'].split(' '):
                    colors[color] += edge[color]
                    edge_colors[color] += edge[color]

                edge['color'] = COLORS[edge_colors.most_common(1)[0][0].lower()]

            graph.node[src]['count'] = count

            if colors:
                graph.node[src]['color'] = COLORS[colors.most_common(1)[0][0].lower()]
            else:
                graph.node[src]['color'] = COLORS['cyan']

        # Dump the parsed graph to a file.
        if args.output is None:
            args.output = self.parse_path(path)
        nx.write_graphml(graph, args.output)

        return "Modfied graph written to {} for Gephi".format(args.output)
