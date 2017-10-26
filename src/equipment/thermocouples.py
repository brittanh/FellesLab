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

@summary       Valves
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

# Define Decorator Functions ------------------------------------------------ #
def j_type_conversion(wrapped):
    """ Decorator performing the conversion from bit value """
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
    meta = { "type": "Temperature",
             "name": "Top",
             "unit": "[C]",
             "channel" : 0,
             "portname" : "--",
             "slaveaddress": "--"
            }

    def __init__(self, portname, slaveaddress, channel, **kwargs):

        if "type" not in kwargs:
            kwargs["type"] = self.__class__.__name__
        if "name" not in kwargs:
            kwargs["name"] = "Address %d Channel %d" %(slaveaddress, channel)
        if "unit" not in kwargs:
            kwargs["unit"] = "--"
        self.__dict__.update(**kwargs)
        self.create_buffer()

        self._sample_raw = int
        self._sample     = float

        super(ThermocoupleBase, self).__init__(portname, slaveaddress, channel)

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

    @property
    def register(self):
        return self.channel

    @register.setter
    def baudrate(self, val):
        self.register = val

    def create_buffer(self, timespan=60):
        length = int(timespan/0.1)
        self._buffer = { 'Time': deque() , 'Temperature': deque() }

    def get_analog_in(self):
        return super(ThermocoupleBase, self).get_analog_in(self.channel)

    @property
    def raw_meassurement(self):
        raw_meassurement = self.get_analog_in()
        return self._raw

    @raw_meassurement.setter
    def raw_meassurement(self):
        self._raw = self.get_analog_in()

    @classmethod
    def resetAll(cls):
        for adaptor in cls.___refs___:
          for key in adaptor._buffer.iterkeys():
            adaptor[key].clear()

# Define Children ----------------------------------------------------------- #
class JType(ThermocoupleBase):

    def get_raw_measurement(self):
        return super(JType, self).get_analog_in()

    @j_type_conversion
    def get_analog_in(self):
        return self.get_raw_measurement()


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

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == '__main__':

    from threading import Thread, Lock, Event, activeCount, local
    from Queue import Queue
    from collections import defaultdict, deque


    class SerialportThread(Thread):
        """ Thread sampling values from ONE serial port """

        RATE = 0.1
        SAVE = True # Event()

        ___refs___ = []

        def __init__ (self, portname):
            super(SerialportThread, self).__init__()

            self.slaves = AdaptorBaseClass.getAdaptors(portname)
            self.portname = portname
            self.daemon = True                          # Use a daemonic thread

            self._data = defaultdict(dict)
            self.events = []

            self.started = time()                              # Set Start time
            self.___refs___.append(self)

            self.start()                                         # Start Thread

        def __setitem__(self, key, val):
            if not key in self._data:
                self._data[key] = val
            else:
                self._data[key].update(val)

        def __getitem__(self, key):
            return self._data[key]

        def sample_loop(self, timestamp, save, *args, **kwargs):
            """
            @brief     Loop over all slaves obtaining MVs
            """

            for slave in self.slaves:
                try:
                    #if self.__class__.SAVE.is_set():
                    #if SerialportThread.SAVE:
                    self[timestamp] = slave.sample(timestamp)
                    #else:
                    #    slave.sample(timestamp, savedata)
                except IOError as e:
                    print("Failed to read measurement:\n\t\t\t\t %s" %(e))
                except SerialException as e:
                    print("Serial Exception")
                    print(e)
                    raise e
                except ValueError as e:
                    print("Value Error")
                    print(e)
                    raise e
                except Exception as e:
                    print("Exception")
                    print(e)
                    raise e

        def run(self):
            """
            @brief Method performing the sampling (executed by `self.start()`).
            """
            while True:
                self.dt = time() - self.started
                self.sample_loop(self.dt, self.__class__.SAVE)         # Sample
                sleep(RATE)                             # Put Thread "to sleep"

        @classmethod
        def set_event(self, adaptor, action, destination):
            self.events.append((adaptor, action))

        @classmethod
        def save_sampling(cls):
            #from csv import DictWriter
            #cls.SAVE.clear()
            cls.SAVE = False
            for thread in cls.___refs___:
                print(thread._data)

        @classmethod
        def start_sampling(cls):
            cls.SAVE = True

        @classmethod
        def pause_sampling(cls):
            cls.SAVE = False

        @classmethod
        def reset_sampling(cls):
            """ """
            #cls.SAVE.clear()
            cls.SAVE = True
            for thread in cls.___refs___:
                for slave in thread.slaves:
                    slave._buffer.clear()
                thread._data.clear()
                thread.started = time()

    def ports():
        return Thermocouple.getPorts()

    def initialize_sampling():
        return [ SerialportThread(port) for port in ports() ]

    def start():
        print("Sampling Started")
        SerialportThread.start_sampling()

    def pause():
        print("Sampling Paused")
        SerialportThread.pause_sampling()

    def save():
        print("Sampling Stopped and Saved")
        SerialportThread.save_sampling()

    def reset():
        print("Sampling Stopped and Deleted")
        SerialportThread.reset_sampling()

    test_adaptor = Thermocouple(
                 portname='/dev/ttyUSB0',
                 slaveaddress=2,
                 channel=0,
                 type= "Temperature",
                 name = "Top",
                 unit = "[C]",
               )

    threads = initialize_sampling()
      
    save()
    pause()
    raw_input()
    start()
    save()
    reset()
    save()

# Vim 'modelines' (Vim will read 5 by default) ------------------------------- #
# vim: filetype=python fileencoding=ascii syntax=on colorcolumn=80
# vim: ff=unix tabstop=4 softtabstop=0 expandtab shiftwidth=4 smarttab
