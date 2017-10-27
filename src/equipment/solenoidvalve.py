#!/usr/bin/python
# -*- coding: ascii -*-
"""
ooooooooooo        oooo oooo                     ooooo                .o8       
`888'    `8        `888 `888                     `888'               "888       
 888      .ooooo.   888  888   .ooooo.   .oooo.o  888        .oooo.   888oooo.  
 888ooo8 d88' `88b  888  888  d88' `88b d88(  "8  888       `P  )88b  d88' `88b 
 888   " 888ooo888  888  888  888ooo888 `"Y88b.   888        .oP"888  888   888 
 888     888    .o  888  888  888    .o o.  )88b  888     o d8(  888  888   888 
o888o    `Y8bod8P' o888oo888o `Y8bod8P' 8""888P' o888ooood8 `Y888""8o `Y8bod8P' 

@brief         Minimal implementation of a Solenoid Valve communication API
@author        Sigve Karolius (SK)
@organization  Department of Chemical Engineering, NTNU, Norway
@contact       sigve.karolius@ntnu.no
@license       Free (GPL.v3) !!! Distributed as-is !!!
@requires      Python 2.7.x or higher
@since         2017-06-16
@change        2017-10-27 (SK) Version bump (1.0), documentation updated
@version       1.0
"""

from felleslab.communication import Adam4069
from collections import deque
import weakref


class SolenoidValve(Adam4069):
    """
    @brief    Communication adaptor for Solenoid Valves
    """
    valve_states = ("Open", "Closed")

    def __init__(self, portname, slaveaddress, channel, **kwargs):
        """
        @brief    Constructor
        @param    portname      str  required  Computer communication port
        @param    slaveaddress  int  required  Module address in the network
        @param    channel       int  required  Communication register in module
        @details
                  The purpose of the constructor is to connect to a module
                  in the RS485 network.

        @todo     Allow key "initialState" in "kwargs", the constructor should
                  ensure that the initial state is set to this value.
        @todo     Consider allowing "finalState" in "kwargs", this could be
                  attached to the "__del__" method, thus ensuring the valve
                  is "fail-open" or "fail-close".
        """
        self.__dict__.update(**kwargs)
        super(SolenoidValve, self).__init__(portname, slaveaddress, channel)


        self._state = self.get_digital_out()

    @property
    def state(self):
        """ Return current state of the valve
        """
        return self._state

    @state.setter
    def state(self, value):
        """
        @brief    Changes the state (set-point) of the valve.
        @details
                  The user-specified change is ignored if the value of the
                  current state is the same, this is done to conserve network
                  communication.
        """
        assert value in (0, 1), "Possible valve states: 0 (open), 1 (close)"

        if value != self.state:
            self.set_digital_out(value)
            self._state = value
        else:
            print("Valve is already %s" %(self.valve_states[value]))

    def setOpen(self):
        """ Method opening the valve
        """
        self.state = 0

    def setClose(self):
        """ Method closing the valve
        """
        self.state = 1

    def getState(self):
        """ Method returning valve state
        """
        return self.state

    def set_digital_out(self, value):
        """
        @brief   Calls the equivalent method in the parent class, thus changing
                 the state of the valve.
        """
        return super(SolenoidValve, self).set_digital_out(self.channel, value)

    def get_digital_out(self):
        """
        @brief   Calls the equivalent method in the parent class, thus querying
                 the state of the valve.
        """
        return super(SolenoidValve, self).get_digital_out(self.channel)

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == '__main__':
    from time import time, sleep
    from serial import SerialException
    from threading import Thread, Lock, Event, activeCount, local
    from Queue import Queue
    from collections import defaultdict, deque

    v = SolenoidValve(
                 portname='/dev/ttyUSB0',
                 slaveaddress=1,
                 channel=0,
                 type= "Binary",
                 name = "Top",
                 unit = "[-]",
               )

