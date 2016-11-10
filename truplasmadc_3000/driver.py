import threading
import time

from slave.driver import Driver
from protocol import TruPlasmaDC3000Protocol
from messages.identification import IdentificationMessage
from messages.normal import NormalMessage
from messages.setfloat import SetFloatMessage
from messages.setint import SetIntMessage
from messages.readfloat import ReadFloatMessage
from messages.readint import ReadIntMessage
from messages.setbyte import SetByteMessage
from messages.readbyte import ReadByteMessage

class TruPlasmaDC3000Driver(Driver):

    def __init__(self, transport, protocol=None):
        if protocol is None:
            protocol = TruPlasmaDC3000Protocol()
        
        self.thread = None
        
        super(TruPlasmaDC3000Driverexit(), self).__init__(transport, protocol)

    def send_message(self, message):
        return self._protocol.query(self._transport, message)
    
    def get_identification(self):
        return self.send_message(IdentificationMessage())
        
    def normal_run(self, voltage, current, power, bits):
        msg = NormalMessage()
        msg.set_voltage(voltage) # U_max = 800 V
        msg.set_current(current) # I_max = 1 A
        msg.set_power(power) # P_max in Watt
        msg.set_bits(bits) # Power On, PC Control On, Profibus Control On, Display Control On
        
        return self.send_message(msg)
    
    """
    def _set_power_single(self, power, current, voltage):
        msg = NormalMessage()
        msg.set_voltage(voltage) # U_max = 800 V
        msg.set_current(current) # I_max = 1 A
        msg.set_power(power) # P_max in Watt
        msg.set_bits(0b01000111) # Power On, PC Control On, Profibus Control On, Display Control On
    
        return self.send_message(msg)
    """
        
    def set_float(self, channel, number):
        msg = SetFloatMessage()
        msg.set_channel(channel)
        msg.set_float(number)
        return self.send_message(msg)
    
    def read_float(self, channel):
        msg = ReadFloatMessage()
        msg.set_channel(channel)
        
        response = self.send_message(msg)
        return response.get_float()
    
    def shutdown(self):
        self.stop_thread()
        self.set_int(1, 2)
        
    def startup(self):
        self.set_int(1, 1)
    
    def set_int(self, channel, number):
        msg = SetIntMessage()
        msg.set_channel(channel)
        msg.set_int(number)
        return self.send_message(msg)
    
    def read_int(self, channel):
        msg = ReadIntMessage()
        msg.set_channel(channel)
        response = self.send_message(msg)
        return response.get_int()
    
    def set_byte(self, channel, number):
        msg = SetByteMessage()
        msg.set_channel(channel)
        msg.set_byte(number)
        return self.send_message(msg)
    
    def read_byte(self, channel):
        msg = ReadByteMessage()
        msg.set_channel(channel)
        response = self.send_message(msg)
        return response.get_byte()
    
    