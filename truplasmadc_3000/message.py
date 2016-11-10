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

import struct

def a2i(number):
    if isinstance(number, str):
        return int(number, 16)
    elif isinstance(number, int):
        return number
    else:
        raise ValueError('Unknown number type')
        
def hex_byte_to_binary(number):
    return struct.pack('>B', number)

def binary_to_hex_byte(binary):
    return struct.unpack('>B', binary)[0]
    
def concate_byte_list(ls):
    return b"".join(ls)

def float_to_hex(number):
    return map(binary_to_hex_byte, struct.pack('<f', number))

def hex_to_float(number):
    return struct.unpack('<f', "".join(map(hex_byte_to_binary, number)))[0]

class Message(object):
    def __init__(self, cmd):
        self.do_allocate(8)
        self.set_length(0)
        self.set_command(cmd)
        
    def do_allocate(self, length):
        self.msg = length*[0]
        
    def set_length(self, number):
        self.msg[0] = a2i(number)
        self.msg[1] = (~ a2i(number)) & 0xff
        
    def set_destination(self, dest):
        self.msg[3] = dest & 0xff
        self.msg[2] = dest >> 8 & 0xff
    
    def get_destination(self):
        return self.msg[2] << 8 | self.msg[3]
        
    def set_source(self, src):
        self.msg[5] = src & 0xff
        self.msg[4] = src >> 8 & 0xff
        
    def get_source(self):
        return self.msg[4] << 8 | self.msg[5]
        
    def set_command(self, cmd):
        self.msg[7] = cmd & 0xff
        self.msg[6] = cmd >> 8 & 0xff
        
    def get_command(self):
        return self.msg[6] << 8 | self.msg[7]
        
    def add_parameter(self, number):
        self.msg.append(number & 0xff)
        
    def get_parameter(self, index):
        return self.msg[index]
        
    def get_message_length(self):
        return self.msg[0]
    
    def get_length(self):
        return len(self.msg)
        
    def compute_crc(self):
        return sum(self.msg[2:]) & 0xffff
    
    def get_crc(self):
        size = len(self.msg)
        return self.msg[size-2] << 8 | self.msg[size-1]
        
    def finish(self):
        crc = self.compute_crc()
        self.msg[len(self.msg)-2] = crc >> 8 & 0xff
        self.msg[len(self.msg)-1] = crc & 0xff
        self.set_length(len(self.msg))
        
    def to_binary(self):
        return concate_byte_list(map(hex_byte_to_binary, self.msg))
    
    def __str__(self):
        return " ".join(map(hex, self.msg))
    
    def response_length(self):
        raise Exception('Not implemented.')
                        
    def create_response(self, bytes):
        raise Exception('Not implemented.')
    
        
class Response(Message):
    
    def __init__(self, binarydata):
        #if packed:
        #    self.msg = map(binary_to_hex_byte, binarydata)
        #else:
            self.msg = binarydata    
    
    def can_handle(self, response):
        if not isinstance(response, Response):
            raise RuntimeError('No Response given')
        return self._can_handle(response)
    
    def _can_handle(self, response):
        raise Exception('Not implemented.')
    
    def get_ack(self):
        return self.msg[6] << 8 | self.msg[7]
    
    def is_ack(self):
        return self.get_ack() == 0x4000
    
    def is_nack(self):
        return not self.is_ack()
    
    def is_valid_crc(self):
        return sum(self.msg[2:self.get_length()-2]) & 0xffff == self.get_crc()
    
    def get_command(self):
        return self.msg[8] << 8 | self.msg[9]