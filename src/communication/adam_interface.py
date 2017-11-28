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



class MyRef(weakref.ref):
    """
    Weakreference class, creates an alias to "referee".
    Understand the class works by considering the following example:
        example.py
        ----------------------------------------------------------------------
        import weakref
        
        class MyRef(weakref.ref):
            def __init__(self, referee, callback=None):
                self.referee = referee
                super(MyRef, self).__init__(referee, callback)
            def __call__(self):
                return self.referee()
        class Referee:
            message = "References are clever"
            def __call__(self):
                return self
            def ChangeMessage(self, msg):
            self.message = msg
        a = Referee()
        b = ExtendedRef(a)
        print b().message
        b().ChangeMessage("A different message")
        print a.message
        ----------------------------------------------------------------------
    """
    
    def __init__(self, referee, callback=None):
        self.referee = referee
        super(MyRef, self).__init__(referee, callback)
    
    def __call__(self):
        """
        Magic method.
        Returns the object that the class referes to. The practical
        implication is that it becomes possible to access the objects methods
        and variables through the reference class.
        """
        return self.referee



class AdaptorBaseClass(object):
    """
    """
    __metaclass__ = ABCMeta
    ___refs___ = []                  # List of all instantiated adaptor objects
    
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
        
        self._id = id(self)
        self.samples = []
        self.portname = self.serial.port
        self.slaveaddress = slaveaddress
    
    def __str__(self):
        return "<type %s at %s>" %(type(self), hex(self._id))
    
    @abstractmethod
    def __repr__(self):
        return "%s%d" %(self.portname,self.slaveaddress)
    
    def __eq__(self, other):
        """
        @brief  Adaptors are equal if the port and address in the network is
        the same.
        """
        return True if repr(self) == repr(other) else False
    
    @classmethod
    def getPorts(cls):
        return set( [ adaptor.portname for adaptor in cls.___refs___] )
    
    
    @classmethod
    def getAdaptors(cls, portname):
        return [ a for a in cls.___refs___ if a.portname == portname ]
    
    @classmethod
    def findAdaptor(cls, _id):
        return [ a for a in cls.___refs___ if a._id == _id ]

# --------------------------------------------------------------------------- #
class AdamAdaptorBase(AdaptorBaseClass):
    """
    """
    
    def __init__(self, portname, slaveaddress, channel):
        
        self.portname = portname
        self.slaveaddress = slaveaddress
        self.channel = channel
        
        super(AdamAdaptorBase, self).__init__(portname, slaveaddress)
    
    def __repr__(self):
        return "%s%d%d" %(self.portname,self.slaveaddress,self.channel)
    
    def __getitem__(self, key):
        return self._buffer[key]
    
    def __setitem__(self, key, val):
        self._buffer[key].append(val)


class AdamAnalogInputModule(AdamAdaptorBase):
    
    def get_analog_in(self, channel, numberOfDecimals=0):
        return self.read_register( 1 - 1 + channel)
    
    def set_type_analog_in(self, channel, value):
        return self.write_register(self.type_analog_in_start_channel - 1 + channel, value)
    
    def get_type_analog_in(self, channel, numberOfDecimals = 0):
        return self.read_register(self.type_analog_in_start_channel - 1 + channel, numberOfDecimals)
    
    def get_burn_out_signal(self, channel):
        return self.read_bit(self.burn_out_signal_start_channel - 1 + channel)

class AdamAnalogOutputModule(AdamAdaptorBase):
    
    def set_analog_out(self, channel, value):
        return self.write_register(self.analog_out_start_channel - 1 + channel, value)
    
    def get_analog_out(self, channel):
        return self.read_register(self.analog_out_start_channel - 1 + channel)
    
    def set_type_analog_out(self, channel, value):
        return self.read_register(self.analog_out_start_channel - 1 + channel, value)
    
    def get_type_analog_out(self, channel):
        return self.read_register(self.analog_out_start_channel - 1 + channel)

class AdamDigitalInputModule(AdamAdaptorBase):
    
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 8
    
    def get_digital_in(self, channel):
        return self.read_bit(self.diginal_in_start_channel - 1 + channel)

class AdamDigitalOutputModule(AdamAdaptorBase):
    
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8
    
    def set_digital_out(self, channel, value):
        return self.write_bit(self.digital_out_start_channel - 1 + channel, value)
    
    def get_digital_out(self, channel):
        return self.read_bit(self.digital_out_start_channel - 1 + channel)

class Adam4117(AdamAnalogInputModule):
    """
    Adam-4117
    """
    analog_in_start_channel = 1
    type_analog_in_start_channel = 201
    burn_out_signal_start_channel = 1
    analog_in_number_of_channels = 8

class Adam4019P(AdamAnalogInputModule):
    """
    ADAM4019 sugar class
    """
    analog_in_start_channel = 1
    type_analog_in_start_channel = 201
    burn_out_signal_start_channel = 1
    analog_in_number_of_channels = 8                 # Number of input channels

class Adam4024(AdamAnalogOutputModule, AdamDigitalInputModule):
    """
    ADAM4024
    """
    analog_in_start_channel = 1
    type_analog_in_start_channel = 201
    burn_out_signal_start_channel = 201
    analog_in_number_of_channels = 4
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 4
    
    def GetOut():
        AdamAnalogOutputModule.get_analog_out()
    
    def GetIn():
        AdamDigitalInputModule.get_digital_in()


class Adam4055(AdamDigitalInputModule, AdamDigitalOutputModule):
    """
    ADAM4055
    """
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8
    diginal_in_start_channel = 1
    digital_in_number_of_channels = 8

class Adam4069(AdamDigitalOutputModule):
    """
        @brief    Data Acquisition Module, Power Relay
        """
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8

# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == '__main__':
    from threading import Thread, Lock, Event, activeCount, local
    from Queue import Queue
    from collections import defaultdict, deque
    
    RATE = 0.1
    
    def temperature(wrapped):
        """ Decorator performing the conversion from bit value """
        def wrap(instance, *args, **kwargs):
            return 760.0*wrapped(instance, *args, **kwargs)/65536
        return wrap
    
    
    class GeneralAdaptorInterface(Adam4019P):
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
            
            super(GeneralAdaptorInterface, self).__init__(portname, slaveaddress, channel)

        @property
        def baudrate(self):
            return self.serial.baudrate
        
        @baudrate.setter
        def test(self, val):
            self.serial.baudrate = val
        
        def create_buffer(self, timespan=60):
            length = int(timespan/RATE)
            self._buffer = { 'Time': deque() , 'Temperature': deque() }
        
        def sample(self, time, *args, **kwargs):
            temp = self.get_analog_in()
            self['Temperature'] = temp
            self['Time'] = time
            return { 'Temperature': temp }
        
        @temperature
        def get_analog_in(self):
            return super(GeneralAdaptorInterface, self).get_analog_in(self.channel)
        
        @classmethod
        def resetAll(cls):
            for adaptor in cls.___refs___:
                for key in adaptor._buffer.iterkeys():
                    adaptor[key].clear()
    
    
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
    return AdaptorBaseClass.getPorts()
    
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
    
    adaptor1 = GeneralAdaptorInterface(
                portname='/dev/ttyUSB0',
                slaveaddress=2,
                channel=0,
                type= "Temperature",
                name = "Top",
                unit = "[C]",
                )
        
    threads = initialize_sampling()

    start()
                                       
    raw_input()
                                       
    save()
    pause()
    raw_input()
    start()
    save()
    reset()
    save()

