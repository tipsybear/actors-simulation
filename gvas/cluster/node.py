# gvas.cluster.node
# Simulation class to model a compute node.
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Fri Dec 04 16:52:45 2015 -0500
#
# Copyright (C) 2015 Allen Leis
# For license information, see LICENSE.txt
#
# ID: node.py [] allen.leis@gmail.com $

"""
Simulation class to model a compute node.
"""

##########################################################################
# Imports
##########################################################################

from .base import Machine
from .network import Address, Message

from gvas.config import settings
from gvas.exceptions import NodeLacksCapacity
from gvas.exceptions import UndeliverableMessage

##########################################################################
# Classes
##########################################################################


class Node(Machine):

    def __init__(self, env, *args, **kwargs):
        self.rack = kwargs.get('rack', None)
        self.cpus = kwargs.get('cpus', settings.defaults.node.cpus)
        self.memory = kwargs.get('memory', settings.defaults.node.memory)
        self.programs = {}
        super(self.__class__, self).__init__(env, *args, **kwargs)

    def send(self, message=None, **kwargs):
        """
        Puts a message onto the parent Rack.

        Interface takes either:
            1. a message object
            2. a destination address, value and size
        """
        if message is None:
            kwargs['src'] = self.address
            message = Message(**kwargs)

        self.rack.send(message)

    def recv(self, message):
        """
        Obtains a message from the parent Rack.
        """
        delivered = False

        if message.dst.pid is not None:
            # Deliver message by process id.
            program = self.programs.get(message.dst.pid, None)
            if program is not None:
                program.recv(message)
                delivered = True

        else:
            # Attempt to deliver by port number
            for program in self.programs.itervalues():
                if message.dst.port in program.ports:
                    program.recv(message)
                    delivered = True

        if not delivered:
            raise UndeliverableMessage(
                "A message was unable to be delivered to {}"
                .format(self.address)
            )

    def assign(self, program):
        """
        Ingests a new Program for processing.  If there aren't enough resources
        available then raises `NodeLacksCapacity`.
        """
        if self.idle_cpus < program.cpus:
            raise NodeLacksCapacity('{} cpus requested but only {} are free.'
                                    .format(program.cpus, self.idle_cpus))

        if self.idle_memory < program.memory:
            raise NodeLacksCapacity('{}GB requested but only {}GB are free.'
                                    .format(program.memory, self.idle_memory))

        self.programs[program.id] = program
        program.node = self

    def run(self):
        """
        Method to kickoff process simulation.
        """
        yield self.env.timeout(1)

    @property
    def address(self):
        """
        Addressable identifier for this node containing the Rack and Node ID.
        """
        return Address(self.rack.id, self.id, None, None)

    @property
    def id(self):
        """
        The unqiue identifier for this instance.

        Note that the _id property is initially set in the NamedProcess
        ancestor class and so all subclasses may share the same Sequence.
        """
        return self._id

    @property
    def idle_cpus(self):
        """
        Number of available CPUs for this node.
        """
        used = sum([p.cpus for p in self.programs.itervalues()])
        return self.cpus - used

    @property
    def idle_memory(self):
        """
        Gigabytes of available memory for this node
        """
        used = sum([p.memory for p in self.programs.itervalues()])
        return self.memory - used

    def __str__(self):
        return "Node: id: {}, cpus={},  memory={}".format(
            self.id,
            self.cpus,
            self.memory
        )

    def __repr__(self):
        return "<{}>".format(self.__str__())


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    import simpy
    env = simpy.Environment()

    factory = Node.create(env, cpus=4, memory=16)
    n = factory.next()

    print n.cpus
    print n.idle_cpus
