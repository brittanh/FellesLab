# -*- coding: ascii -*-
"""
ooooooooooo        oooo oooo                     ooooo                .o8
`888'    `8        `888 `888                     `888'               "888
 888      .ooooo.   888  888   .ooooo.   .oooo.o  888        .oooo.   888oooo.
 888ooo8 d88' `88b  888  888  d88' `88b d88(  "8  888       `P  )88b  d88' `88b
 888   " 888ooo888  888  888  888ooo888 `"Y88b.   888        .oP"888  888   888
 888     888    .o  888  888  888    .o o.  )88b  888     o d8(  888  888   888
o888o    `Y8bod8P' o888oo888o `Y8bod8P' 8""888P' o888ooood8 `Y888""8o `Y8bod8P'

@summary       Bare-Bones module facilitating Modbus-RTU communication with
               Advantech ADAM-4000 and ADAM-4100 modules
@author:       Sigve Karolius
@organization  Department of Chemical Engineering, NTNU, Norway
@contact       sigve.karolius@ntnu.no
@license       Free (GPL.v3) !!! Distributed as-is !!!
@requires      Python 2.7.x or higher
@since         2017-06-16
@version       0.1
@details
               > This package only supports the RTU Modbus protocol.


               A "slave" is connected to a serial port in a 

               Adam4019(<portname>, <slaveaddress>, <channel>)

               Adam4019('/dev/ttyUSB0', 4, 0)

               This will start a [thread] whose job it is to rule the serial-
               port '/dev/ttyUSB0'

               Subsequent creation of instances, such as:

               Adam4019('/dev/ttyUSB0', 1, 0)
               Adam4019('/dev/ttyUSB0', 2, 0)               
               Adam4019('/dev/ttyUSB0', 3, 0)

               Will also be sampled by the "master" thread


the thread acts as a rudimentary state-machine, sampling the slaves sequentially and responds to events as they appear.


"""
from time import sleep, time

from minimalmodbus import Instrument
from serial import SerialException
from serial.tools.list_ports import comports
from random import random, randint
from abc import ABCMeta, abstractmethod
import weakref

# --------------------------------------------------------------------------- #
#LOCK = Lock() # Lock
#KILL = Event()
#SAVE = False
#RATE = 0.1

# TODO: Implement a thorough test ensuring that we have access to a serial port
DUMMY_RUN = True if not comports() else False
#

STATE = {"Idle", "Save"}

# --------------------------------------------------------------------------- #

class DummySerial(object):
    """ Dummy class impersonating a serial connection (for consistency) """
    port = 'Dummy'                                           # serial port name
    baudrate = 9600                                     # Transfer rate: bits/s
    bytesize = 8                                               # bits in a byte
    parity = 'N'#minimalmodbus.serial.PARITY_NONE                # the same as: 'N'
    timeout = 0.05                                                    # seconds
    mode = 'rtu'#minimalmodbus.MODE_RTU                 # or minimalmodbus.MODE_ASCII

    def flushOutput(self):
        pass

    def flushInput(self):
        pass

    def write(self, message):
        pass

    def read(self):
        return 'FooBar'


class DummyModbus(object):
    """ Dummy class impersonating a Adam module """

    def __init__(self, *args, **kwargs):
        self.slaveaddress = 'slaveaddress'
        self.portname = 'portname'
        self.serial = DummySerial()

    def read_register(self, channel):
        return randint(0, 65536)

    def read_registers(self, channel, number_of_channels):
        return random()

    def read_bit(self, channel):
        return randint(0, 1)

    def read_float(self, channel):
        return random()

    def read_long(self, channel):
        return random()

    def read_string(self, channel):
        return random()

    def write_float(self, channel, value):
        pass

    def write_long(self, channel, value):
        pass

    def write_registers(self, channel, value):
        pass

    def write_string(self, channel, value):
        pass

    def write_register(self, channel, value):
        pass

    def write_bit(self, channel, value):
        pass

    def flushOutput(self):
        pass

    def flushInput(self):
        pass

    def write(self, msg):
        pass

    def read(self):
        pass


class AdaptorBaseClass(object):
    """
    """

    def __new__(cls, *args, **kwargs):
        """
        Called !!before!! __init__, returns instance.

        Changes the "type" of the class according to 'base', default is to
        attempt connecting to the AdamModule, however, it is possible to
        add an argument "Dummy" for "simulating" the Adam module.

        This is how it looks like:
          < adam_modules.adam_modules.'MODULE' + 'BASE' object at ... >
            MODULE: Adam4019 etc...
            MODE: Dummy or Instrument
        """
        addCls = DummyModbus if DUMMY_RUN else Instrument
        cls = type(cls.__name__ + '+' + addCls.__name__, (cls, addCls), {})
        return  super(AdaptorBaseClass, cls).__new__(cls)

    def __init__(self, portname, slaveaddress):
        super(AdaptorBaseClass, self).__init__(portname, slaveaddress)
        

        self.portname     = self.serial.port
        self.slaveaddress = slaveaddress

    @property
    def port(self):
        return self.serial.port

    @port.setter
    def port(self, portname):
        self.serial.port = portname

    @property
    def baudrate(self):
        return self.serial.baudrate

    @baudrate.setter
    def baudrate(self, val):
        self.serial.baudrate = val

    def __str__(self):
        return "<type %s at %s>" %(type(self), hex(self._id))

