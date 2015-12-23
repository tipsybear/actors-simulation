# gvas.utils.graph
# Network graph utility for visualizing communications between nodes.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Tue Dec 22 16:23:49 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: graph.py [] benjamin@bengfort.com $

"""
Network graph utility for visualizing communications between nodes.
"""

##########################################################################
## Imports
##########################################################################

import networkx as nx

from datetime import datetime
from gvas.cluster.network import Address
from gvas.utils.timez import HUMAN_DATETIME

##########################################################################
## Module Constants
##########################################################################

SOURCE_ADDR = Address("source", "source", "source", "STREAM")

##########################################################################
## Message Specific NetworkX Graph
##########################################################################

def stringify_address(addr):
    """
    Stringifies the address namedtuple into a representation that can be used
    for a nodeid in the graph. The specification is then stored as node attrs.
    """
    if addr == SOURCE_ADDR:
        return addr.pid
    return "{}@{}.{}:{}".format(addr.pid, addr.rack, addr.node, addr.port)


class CommsGraph(nx.DiGraph):
    """
    Extends the directed graph in NetworkX to deal with messages in the
    network for visualization and other graph based analyses.
    """

    @classmethod
    def load(klass, path):
        """
        Loads a graph from a GraphML file on disk, and converts it to a comms
        graph class (a subclass of digraph).

        TODO: figure out how to convert the graph.
        """
        g = nx.read_graphml(path)
        assert isinstance(g, nx.DiGraph)
        raise NotImplementedError("Still need to do graph conversion.")

    def dump(self, path, **kwargs):
        """
        Dumps the communications graph to a GraphML file at the specified
        path. Can pass any argument into the serialization (e.g. prettyprint
        or encoding specification). This method does not natively compress
        the graphml output, but it can if required.
        """
        # Before we can write, we need to deal with unwritable data types.
        for src, dst in self.edges():
            self[src][dst]['color'] = ' '.join(self[src][dst]['color'])

        nx.write_graphml(self, path, **kwargs)

    def __init__(self, data=None, **attrs):
        attrs['title']   = attrs.pop('title', 'GVAS Communication Graph')
        attrs['created'] = attrs.pop('created', datetime.now().strftime(HUMAN_DATETIME))
        super(CommsGraph, self).__init__(data, **attrs)

    def add_message(self, msg):
        """
        Helper method for adding a message between two nodes.
        TODO: Clean this up, it's kind of a mess.
        """
        # Check if the source is None, e.g. from a Stream
        if msg.src is None:
            msg = msg._replace(src=SOURCE_ADDR)

        # Create source and dest address mapping
        addrs = {}

        # Check if source and destination are nodes in the graph
        # Add them, expanding their attrs if not and adding to mapping
        for key in ('src', 'dst'):
            # Fetch address and update the mapping
            addr = getattr(msg, key)
            addrs[key] = stringify_address(addr)

            # Check if the node exists, otherwise add it.
            if not self.has_node(addrs[key]):
                attrs = dict(zip(addr._fields, addr))
                self.add_node(addrs[key], **attrs)

        # Create the attributes dictionary for the edge
        attrs = dict(zip(msg._fields, msg))

        # Remove the src and dst from the attributes
        for key in ('src', 'dst'): attrs.pop(key)

        # Change the colors into a list and add color count attributes
        attrs['color'] = [attrs['color']] if attrs.get('color', None) else []
        for color in attrs['color']: attrs[color] = 1

        # Count the number of messages between these nodes
        attrs['count'] = 1

        # If the edge already exists, update the attrs with previous values.
        if self.has_edge(addrs['src'], addrs['dst']):
            oldattrs = self[addrs['src']][addrs['dst']]

            # Update the node count, size, and value totals
            attrs['count'] += oldattrs['count']
            attrs['value'] += oldattrs['value']
            attrs['size']  += oldattrs['size']

            # Update the colors list
            attrs['color'].extend(oldattrs['color'])
            attrs['color'] = list(set(attrs['color']))

            for color in attrs['color']:
                attrs[color] = attrs.get(color, 0) + oldattrs.get(color, 0)

        # Add or update the edge with the new attrs.
        self.add_edge(addrs['src'], addrs['dst'], **attrs)
