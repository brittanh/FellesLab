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

@summary       Thermocouple
@author:       Sigve Karolius
@organization  Department of Chemical Engineering, NTNU, Norway
@contact       sigve.karolius@ntnu.no
@license       Free (GPL.v3) !!! Distributed as-is !!!
@requires      Python 2.7.x or higher
@since         2017-06-16
@version       0.1

"""
from felleslab.communication import Adam4019P
from collections import deque

from serial import SerialException

# Define Decorator Functions ------------------------------------------------ #
def j_type_conversion(wrapped):
    """ Decorator performing the conversion from bit value
    """
    def wrap(instance, *args, **kwargs):
        return 760.0*wrapped(instance, *args, **kwargs)/65536
    return wrap

def k_type_conversion(wrapped):
    """ Decorator performing the conversion from bit value """
    def wrap(instance, *args, **kwargs):
        return 1360.0*wrapped(instance, *args, **kwargs)/65536
    return wrap

def t_type_conversion(wrapped):
    """ Decorator performing the conversion from bit value """
    def wrap(instance, *args, **kwargs):
        return (400 - (-100.))*wrapped(instance, *args, **kwargs)/65535 - 100
    return wrap

# Define Base Class --------------------------------------------------------- #
class ThermocoupleBase(Adam4019P):
    """
    """

    _state_raw = int
    _state     = float
    _setpoint  = float

    def __init__(self, portname, slaveaddress, channel, **kwargs):
        super(ThermocoupleBase, self).__init__(portname, slaveaddress, channel)

    @property
    def state(self):
        try:
          ret = self.get_analog_in()
        except SerialException:
          print("Temperature measurement failed")
          ret = "NA"
        return ret

    @property
    def raw_meassurement(self):
        self._raw = super(ThermocoupleBase, self).get_analog_in(self.channel)
        return self._raw

    @raw_meassurement.setter
    def raw_meassurement(self):
        self._raw = self.get_analog_in()

    def get_analog_in(self):
        return super(ThermocoupleBase, self).get_analog_in(self.channel)


# Define Children ----------------------------------------------------------- #
class JType(ThermocoupleBase):

    @j_type_conversion
    def get_analog_in(self):
        return super(JType, self).get_analog_in()


class KType(ThermocoupleBase):

    def get_raw_measurement(self):
        return super(KType, self).get_analog_in()

    @k_type_conversion
    def get_analog_in(self):
        return self.get_raw_measurement()


class TType(ThermocoupleBase):

    def get_raw_measurement(self):
        return super(TType, self).get_analog_in()

    @t_type_conversion
    def get_analog_in(self):
        return self.get_raw_measurement()


# Vim 'modelines' (Vim will read 5 by default) ------------------------------- #
# vim: filetype=python fileencoding=ascii syntax=on colorcolumn=80
# vim: ff=unix tabstop=4 softtabstop=0 expandtab shiftwidth=4 smarttab
