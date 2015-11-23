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

from gvas.dynamo import Sequence, Uniform
from gvas.base import Process, NamedProcess
from gvas.base import Simulation

##########################################################################
## Simulation Configuration
##########################################################################

GAS_STATION_SIZE = 100          # Gallons
THRESHOLD        = 15           # Thresdhold for calling tank truck (in %)
FUEL_TANK_SIZE   = 14           # Gallons
FUELTANK_LEVEL   = (2, 9)       # Min/max levels of fuel tanks (in gallons)
REFUELING_SPEED  = 0.1667       # Gallons per second
TANK_TRUCK_TIME  = 300          # Seconds it takes fuel truck to arrive
T_INTER          = (30, 300)    # Create a car every min/max Seconds


##########################################################################
## Simulation Processes
##########################################################################


class Car(NamedProcess):
    """
    A car is a utilizer of gas station resources.
    """

    def __init__(self, env, station):
        self.station    = station
        self.fuel_level = Uniform(*FUELTANK_LEVEL).get()

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
            start = self.env.now

            # request one of the gas pumps
            yield req

            # Get the required amount of fuel
            gallons_required = FUEL_TANK_SIZE - self.fuel_level
            yield self.station.pump.get(gallons_required)

            # The "actual" refueling process takes some time
            yield self.env.timeout(gallons_required / REFUELING_SPEED)

            print "{} finished refueling in {:0.1f} seconds.".format(
                self.name, self.env.now - start
            )


class CarGenerator(Process):
    """
    Generates new cars that arrive at the gas station.
    """

    def __init__(self, env, station):
        self.station = station
        self.uniform = Uniform(*T_INTER)
        super(CarGenerator, self).__init__(env)

    def run(self):
        """
        Create a new car at the station at each random interval.
        """
        for idx in Sequence():
            yield self.env.timeout(self.uniform.get())
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
                print "Calling the tank truck at {} (station at {}%)".format(self.env.now, self.station.percent_full())
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


##########################################################################
## Simulation
##########################################################################

class GasStationSimulation(Simulation):

    def script(self):
        bcs = GasStation(self.env)
        GasStationControl(self.env, bcs)
        CarGenerator(self.env, bcs)


if __name__ == '__main__':
    # Setup and start the simulation
    sim = GasStationSimulation()
    sim.run()
