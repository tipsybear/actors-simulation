# gvas.sims.cars
# The tutorial simulation from SimPy to frame running simulations.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Sun Nov 22 11:58:58 2015 -0500
#
# Copyright (C) 2015 University of Maryland
# For license information, see LICENSE.txt
#
# ID: cars.py [] benjamin@bengfort.com $

"""
The tutorial simulation from SimPy to frame running simulations. This
simulation models electric vehicles, but shows the basic mechanism for
running a GVAS simulation using a known environment/tutorial.

TODO: Deprecate this simulation, it is just a stub.
"""

##########################################################################
## Imports
##########################################################################

import simpy
import random

##########################################################################
## Simulation Configuration
##########################################################################

RANDOM_SEED      = 42
GAS_STATION_SIZE = 100          # Gallons
THRESHOLD        = 15           # Thresdhold for calling tank truck (in %)
FUEL_TANK_SIZE   = 14           # Gallons
FUELTANK_LEVEL   = (2, 9)       # Min/max levels of fuel tanks (in gallons)
REFUELING_SPEED  = 0.1667       # Gallons per second
TANK_TRUCK_TIME  = 300          # Seconds it takes fuel truck to arrive
T_INTER          = (30, 300)    # Create a car every min/max Seconds
SIM_TIME         = 5000         # Simulation time in seconds.


##########################################################################
## Helper Objects
##########################################################################

class Sequence(object):
    """
    An infinite sequence and counter object.
    This is a bit more logic wrapped around `itertools.count()`
    """

    def __init__(self, start=0, end=None, step=1):
        self.value    = start
        self.step     = 1
        self.terminal = end

    def next(self):
        self.value += self.step

        if self.terminal is not None and self.value > self.terminal:
            raise StopIteration("Stepped beyond terminal value!")

        return self.value

    def __iter__(self):
        return self


class Process(object):
    """
    Base process object.
    """

    def __init__(self, env):
        self.env    = env
        self.action = env.process(self.run())


class NamedProcess(Process):
    """
    A process with a sequence counter and self identification.
    """

    counter = Sequence()

    def __init__(self, env):
        self._id = self.counter.next()
        super(NamedProcess, self).__init__(env)

    @property
    def name(self):
        return "{} #{}".format(self.__class__.__name__, self._id)

##########################################################################
## Simulation Processes
##########################################################################


class Car(NamedProcess):
    """
    A car is a utilizer of gas station resources.
    """

    def __init__(self, env, station):
        self.station    = station
        self.fuel_level = random.randint(*FUELTANK_LEVEL)

        super(Car, self).__init__(env)


    def run(self):
        """
        A car arrives at the gas station for refueling. It requests one of
        the gas station's fuel pumps and tries to get the desired amount of
        gas from it. If the station's reservoir is empty, then it has to wait
        for the tank truck to arrive.
        """
        print "{} arrived at gas station at {:0.1f}".format(self.name, self.env.now)
        with self.station.request() as req:
            start = env.now

            # request one of the gas pumps
            yield req

            # Get the required amount of fuel
            gallons_required = FUEL_TANK_SIZE - self.fuel_level
            yield self.station.pump.get(gallons_required)

            # The "actual" refueling process takes some time
            yield env.timeout(gallons_required / REFUELING_SPEED)

            print "{} finished refueling in {:0.1f} seconds.".format(
                self.name, self.env.now - start
            )


class CarGenerator(Process):
    """
    Generates new cars that arrive at the gas station.
    """

    def __init__(self, env, station):
        self.station = station
        super(CarGenerator, self).__init__(env)

    def run(self):
        """
        Create a new car at the station at each random interval.
        """
        for idx in Sequence():
            yield env.timeout(random.randint(*T_INTER))
            Car(self.env, self.station)


class TankTruck(Process):
    """
    Arrives at the gas station after a delay and refuels.
    """

    def __init__(self, env, station):
        self.station = station
        super(TankTruck, self).__init__(env)

    def run(self):
        yield self.env.timeout(TANK_TRUCK_TIME)
        print "Tank truck arriving at {}".format(self.env.now)
        amount = self.station.pump.capacity - self.station.pump.level
        print "Tank truck refuelling {:0.1f} gallons".format(amount)
        yield self.station.pump.put(amount)


class GasStationControl(Process):
    """
    Periodically check the level of the pump and call the tank truck if the
    level falls below a certain threshold level.
    """

    def __init__(self, env, station):
        self.station = station
        super(GasStationControl, self).__init__(env)

    def run(self):
        while True:
            if self.station.percent_full() < THRESHOLD:
                # Call the tank truck!
                print "Calling the tank truck at {} (station at {}%)".format(env.now, self.station.percent_full())
                yield TankTruck(self.env, self.station).action

            yield self.env.timeout(10) # Check every 10 seconds

##########################################################################
## Simulation Resources
##########################################################################

class GasStation(simpy.Resource):

    def __init__(self, env, capacity=2):
        super(GasStation, self).__init__(env, capacity=capacity)
        self.pump = simpy.Container(env, GAS_STATION_SIZE, init=GAS_STATION_SIZE)

    def percent_full(self):
        return (float(self.pump.level) / float(self.pump.capacity)) * 100

if __name__ == '__main__':
    # Setup and start the simulation
    print "Gas Station Simulation"
    random.seed(RANDOM_SEED)

    # Create environment and start processes.
    env = simpy.Environment()
    bcs = GasStation(env)
    GasStationControl(env, bcs)
    CarGenerator(env, bcs)

    # Execute!
    env.run(until=SIM_TIME)
