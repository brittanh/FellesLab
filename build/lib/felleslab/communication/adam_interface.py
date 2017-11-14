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
from adaptor_base import AdaptorBaseClass

# Define Base Class --------------------------------------------------------- #
class AdamAdaptorBase(AdaptorBaseClass):
    """
    @brief    Base class for the Advantech ADAM modules.
    @details
              The modules 
    """

    def __init__(self, portname, slaveaddress, channel):
        """
        """
        self.channel = channel
        super(AdamAdaptorBase, self).__init__(portname, slaveaddress)

# Define Module Types ------------------------------------------------------- #
class AdamAnalogInput(AdamAdaptorBase):
    """
    """

    def get_analog_in(self, channel, numberOfDecimals=0):
        return self.read_register( 1 - 1 + channel)

    def set_type_analog_in(self, channel, value):
        self.write_register(self.type_analog_in_start_channel - 1 + channel, value)

    def get_type_analog_in(self, channel, numberOfDecimals = 0):
        return self.read_register(self.type_analog_in_start_channel - 1 + channel, numberOfDecimals)

    def get_burn_out_signal(self, channel):
        return self.read_bit(self.burn_out_signal_start_channel - 1 + channel)

class AdamAnalogOutput(AdamAdaptorBase):
    """
    """
    analog_out_start_channel = 1

    def set_analog_out(self, channel, value):
        self.write_register(self.analog_out_start_channel - 1 + channel, value)

    def get_analog_out(self, channel):
        return self.read_register(self.analog_out_start_channel - 1 + channel)

    def set_type_analog_out(self, channel, value):
        self.read_register(self.analog_out_start_channel - 1 + channel, value)

    def get_type_analog_out(self, channel):
        return self.read_register(self.analog_out_start_channel - 1 + channel)

class AdamDigitalInput(AdamAdaptorBase):
    """
    """

    diginal_in_start_channel      = 1
    digital_in_number_of_channels = 8

    def get_digital_in(self, channel):
        return self.read_bit(self.diginal_in_start_channel - 1 + channel)

class AdamDigitalOutput(AdamAdaptorBase):
    """
    """

    digital_out_start_channel      = 17
    digital_out_number_of_channels = 8

    def set_digital_out(self, channel, value):
        return self.write_bit(self.digital_out_start_channel - 1 + channel, value)

    def get_digital_out(self, channel):
        return self.read_bit(self.digital_out_start_channel - 1 + channel)

# Define Adam Modules ------------------------------------------------------- #
class Adam4117(AdamAnalogInput):
    """
    Adam-4117
    """
    analog_in_start_channel       = 1
    type_analog_in_start_channel  = 201
    burn_out_signal_start_channel = 1
    analog_in_number_of_channels  = 8

class Adam4019P(AdamAnalogInput):
    """
    @brief    Sugar class for the ADAM 4019+ analog/digital (AD) converter
    @details
              The module has eight (8) optically decoupled input channels that
              can be individually specified to cover the following ranges:

              +-------+---------+---------+
              | Input | Minimum | Maximum |
              |:------|--------:|--------:|
              | Volt  |      -5 |       5 |
              | Volt  |     -10 |      10 |
              +-------+---------+---------+

              The resolution of the storage registers is 16 bit and the module
              provides replies as binary integers. Consequently, the
              minimum value, e.g. -10 [V], corresponds to 0 (zero) and the
              largest value, e.f. +10 [V], is 65536.

              The conversion to voltage is trivial (linear relationship) and
              the user is asked to do that themselves.

    @warning  There is no way for this module to check the internal settings
              of the AD converter. This must be done using Advantech software.
    """
    analog_in_start_channel       = int(1)
    type_analog_in_start_channel  = int(201)
    burn_out_signal_start_channel = int(1)
    analog_in_number_of_channels  = int(8)

    def get_analog_in(self, decimals = 0):
        """
        @brief    Convenience method for querying an analog input.
        @details
                  The method simply calls the equivalent method in the parent
                  class, but automatically passes the channel which is stored
                  in the object.
        """
        return super(Adam4019P, self).get_analog_in(self.channel, decimals)

class Adam4024(AdamAnalogOutput, AdamDigitalInput):
    """
    @brief    Sugar class for the ADAM 4024 analog output module
    @details
              The module has four (4) analog output channels whose registers
              have 12 bit size. This corresponds to integer values in the
              range 0 -- 4096.
    """
    analog_out_start_channel      = int(1)
    analog_in_start_channel       = int(1)
    type_analog_in_start_channel  = int(201)
    burn_out_signal_start_channel = int(201)
    analog_in_number_of_channels  = int(4)
    diginal_in_start_channel      = int(1)
    digital_in_number_of_channels = int(4)

    mode = {'A': {'min': 0, 'max': 20, 'unit': 'Ampere'},
            'B': {'min': 4, 'max': 20, 'unit': 'Ampere'},
            'C': {'min': 0, 'max': 10, 'unit': 'Volt'},
           }


    def set_analog_out(self, value):
        assert type(value) is int, "Only integers are accepted"
        assert value in range(0, 4096), "Allowed range: [0, 4096]"
        super(Adam4024, self).set_analog_out(self.channel, value)

    def get_analog_out(self):
        return super(Adam4024, self).get_analog_out(self.channel)

    def set_type_analog_out(self, value):
        super(Adam4024, self).set_type_analog_out(self.channel, value)

    def get_type_analog_out(self):
        return super(Adam4024, self).get_type_analog_out(self.channel)

    def get_digital_in(self):
        return super(Adam4024, self).get_digital_in(self.channel)

class Adam4055(AdamDigitalInput, AdamDigitalOutput):
    """
    @brief    Sugar class for the ADAM 4055 digital input/output module
    @details
    """
    digital_out_start_channel      = int(17)
    digital_out_number_of_channels = int(8)
    diginal_in_start_channel       = int(1)
    digital_in_number_of_channels  = int(8)

class Adam4069(AdamDigitalOutput):
    """
    @brief    Data Acquisition Module, Power Relay
    """
    digital_out_start_channel = 17
    digital_out_number_of_channels = 8

    def set_digital_out(self, value):
        """
        @brief   Calls the equivalent method in the parent class, thus changing
                 the state of the valve.
        """
        super(Adam4069, self).set_digital_out(self.channel, value)

    def get_digital_out(self):
        """
        @brief   Calls the equivalent method in the parent class, thus querying
                 the state of the valve.
        """
        return super(Adam4069, self).get_digital_out(self.channel)


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: #
if __name__ == '__main__':
    from threading import Thread, Lock, Event, activeCount, local
    from Queue import Queue
    from collections import defaultdict, deque


    def temperature(wrapped):
        """ Decorator performing the conversion from bit value """
        def wrap(instance, *args, **kwargs):
            return 760.0*wrapped(instance, *args, **kwargs)/65536
        return wrap


    class Temperature(Adam4019P):
        meta = { "type": "Temperature",
                 "name": "Top",
                 "unit": "[C]",
                 "channel" : 0,
                 "portname" : "--",
                 "slaveaddress": "--"
                }

        _state = float
        _raw   = int

        def __init__(self, portname, slaveaddress, channel):
            """
            @brief    Constructor
            """
            self.channel = channel
            super(Temperature, self).__init__(portname, slaveaddress, channel)

            _raw = self.get_analog_in(self.channel)

        @property
        def state(self):
            return self._state

        @state.setter
        def state(self):
            self._state = self.get_analog_in()

        @property
        def raw(self):
            return self._raw

        @raw.setter
        def raw(self, val):
            self._raw = self.val


    adaptor1 = Temperature(
                 portname='/dev/ttyUSB0',
                 slaveaddress=2,
                 channel=0,
                 type= "Temperature",
                 name = "Top",
                 unit = "[C]",
               )
