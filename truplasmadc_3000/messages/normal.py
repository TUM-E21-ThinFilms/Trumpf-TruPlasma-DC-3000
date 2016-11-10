# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from truplasmadc_3000.message import Message, Response, hex_to_float, float_to_hex

class NormalMessage(Message):
    def __init__(self):
        self.do_allocate(23)
        self.set_command(0x6040)
        
    def set_voltage(self, number):
        self.msg[8:12] = float_to_hex(float(number))
        
    def get_voltage(self):
        return hex_to_float(self.msg[8:12])
    
    def set_current(self, number):
        self.msg[12:16] = float_to_hex(float(number))
        
    def get_current(self):
        return hex_to_float(self.msg[12:16])
    
    def set_power(self, number):
        self.msg[16:20] = float_to_hex(float(number))
        
    def set_bits(self, number):
        self.msg[20] = int(number) & 0xff
        
    def get_bits(self):
        return self.msg[20]
        
    def get_power(self):
        return hex_to_float(self.msg[16:20])
    
    def response_length(self):
        return 39
    
    def create_response(self, bytes):
        return NormalResponse(bytes)
    
class NormalResponse(Response):
    def get_voltage(self):
        return hex_to_float(self.msg[10:14])
    
    def get_current(self):
        return hex_to_float(self.msg[14:18])
    
    def get_power(self):
        return hex_to_float(self.msg[18:22])
    
    def get_bits_ack(self, bitnumber):
        if bitnumber < 0 or bitnumber > 2:
            raise ValueError('bitnumber has to be in range 0..2')        
        return self.msg[22+bitnumber]
    
    def get_arc_counter(self):
        return self.msg[25] << 8 | self.msg[26]

    def _can_handle(self, response):
        return response.get_command() == 0x6040
