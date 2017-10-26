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
@author        Sigve Karolius
@organization  Department of Chemical Engineering, NTNU, Norway
@contact       sigve.karolius@ntnu.no
@license       Free (GPL.v3) !!! Distributed as-is !!!
@requires      Python 2.7.x or higher
@since         2017-06-16
@version       0.1

"""

from felleslab.communication import Adam4069
from collections import deque
import weakref


class SolenoidValve(Adam4069):
    """
    """
    event_queue = [] # ( event, reply )

    meta = { "type": "Position",
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
        super(SolenoidValve, self).__init__(portname, slaveaddress, channel)

    @property
    def baudrate(self):
        return self.serial.baudrate

    @baudrate.setter
    def baudrate(self, val):
        self.serial.baudrate = val

    def create_buffer(self, timespan=60):
        length = int(timespan/0.1)
        self._buffer = { 'Time': deque() , 'Position': deque() }

    def set_digital_out(self, value):
        return super(SolenoidValve, self).set_digital_out(self.channel, value)

    def get_digital_out(self):
        return super(SolenoidValve, self).get_digital_out(self.channel)

    def sample(self, time, *args, **kwargs):
        raw = self.get_digital_out()
        self['Position'].append(raw)
        self['Time'].append(time)
        return { 'Position': raw }

    def setOpen(self):
        self.set_digital_out(0)

    def setClose(self):
        self.set_digital_out(1)

    def getState(self):
        return self.get_digital_out()

    def onInit(self):
        print("Initialising solenoid valve")
        #self.writeOn()

    def onEvent(self):
        """ Iterate over all events """
        while self.event_queue:
            event, reply = self.event_queue.pop(0)
            ret = event()
            if not reply:
                continue
            reply()

    def onQuit(self):
        print("Shutting down solenoid valve")
        #self.writeOff()

    @classmethod
    def resetAll(cls):
        for adaptor in cls.___refs___:
          for key in adaptor._buffer.iterkeys():
            adaptor[key].clear()

    def __del__(self):
        print("")
        print("Bye bye")
        print("")

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == '__main__':
    from time import time, sleep
    from serial import SerialException
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

            self.slaves = SolenoidValve.getAdaptors(portname)
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
                    if not save:
                        slave().sample(timestamp)
                    else:
                        self[timestamp] = slave().sample(timestamp)
                except Exception as e:
                    raise e

        def event_loop(self):
            """
            @brief     Loop over all slaves obtaining MVs
            """

            for slave in self.slaves:
                try:
                    slave().onEvent()
                except Exception as e:
                    pass

        def run(self):
            """
            @brief Method performing the sampling (executed by `self.start()`).
            """
            while True:
                self.dt = time() - self.started
                self.sample_loop(self.dt, self.__class__.SAVE)         # Sample
                self.event_loop()         # Sample
                sleep(0.1)                             # Put Thread "to sleep"


        @classmethod
        def onQuit(cls):
            for thread in cls.___refs___:
                for slave in thread.slaves:
                    slave().event_queue.append((slave().onQuit, None))

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
                    slave()._buffer.clear()
                thread._data.clear()
                thread.started = time()


    def reply(arg):
        print arg

    def ports():
        return SolenoidValve.getPorts()

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

    test_adaptor = SolenoidValve(
                 portname='/dev/ttyUSB0',
                 slaveaddress=1,
                 channel=0,
                 type= "Binary",
                 name = "Top",
                 unit = "[-]",
               )

    test_adaptor2 = SolenoidValve(
                 portname='/dev/ttyUSB0',
                 slaveaddress=1,
                 channel=1,
                 type= "Binary",
                 name = "Top",
                 unit = "[-]",
               )

    threads = initialize_sampling()

    pause()
    raw_input()
    test_adaptor.event_queue.append((test_adaptor.getState, reply))
    raw_input()
    SerialportThread.onQuit()
    raw_input()
    start()
    save()
    reset()
    save()
