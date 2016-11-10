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

class SetByteMessage(Message):
    def __init__(self):
        self.do_allocate(13)
        self.set_command(0x6111)
        
    def set_channel(self, number):
        self.msg[8] = (number >> 8) & 0xFF
        self.msg[9] = number & 0xFF
        
    def get_channel(self):
        return self.msg[8] << 8 | self.msg[9]
    
    def set_byte(self, number):
        self.msg[10] = number & 0xFF
        
    def get_byte(self):
        return self.msg[10]
       
    def response_length(self):
        return 14
    
    def create_response(self, bytes):
        return SetByteResponse(bytes)
        
class SetByteResponse(Response):
    
    def get_channel(self):
        return self.msg[10] << 8 | self.msg[11]
    
    def _can_handle(self, response):
        return response.get_command() == 0x6111
                           
