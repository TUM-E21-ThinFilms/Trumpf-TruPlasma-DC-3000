from truplasmadc_3000.message import Message, Response, hex_to_float, float_to_hex

class ReadByteMessage(Message):
    def __init__(self):
        self.do_allocate(12)
        self.set_command(0x6112)
        
    def set_channel(self, number):
        self.msg[8] = (number >> 8) & 0xFF
        self.msg[9] = number & 0xFF
        
    def get_channel(self):
        return self.msg[8] << 8 | self.msg[9]
           
    def response_length(self):
        return 15
    
    def create_response(self, bytes):
        return ReadByteResponse(bytes)
        
class ReadByteResponse(Response):
    
    def get_channel(self):
        return self.msg[10] << 8 | self.msg[11]
    
    def get_byte(self):
        return self.msg[12]
    
    def _can_handle(self, response):
        return response.get_command() == 0x6112
                           
