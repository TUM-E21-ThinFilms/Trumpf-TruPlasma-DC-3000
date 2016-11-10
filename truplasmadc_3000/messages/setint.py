from truplasmadc_3000.message import Message, Response, hex_to_float, float_to_hex

class SetIntMessage(Message):
    def __init__(self):
        self.do_allocate(14)
        self.set_command(0x6121)
        
    def set_channel(self, number):
        self.msg[8] = (number >> 8) & 0xFF
        self.msg[9] = number & 0xFF
        
    def get_channel(self):
        return self.msg[8] << 8 | self.msg[9]
    
    def set_int(self, number):
        self.msg[10] = (number >> 8) & 0xFF
        self.msg[11] = (number) & 0xFF
        
    def get_int(self):
        return self.msg[10] << 8 | self.msg[11]
           
    def response_length(self):
        return 14
    
    def create_response(self, bytes):
        return SetIntResponse(bytes)
        
class SetIntResponse(Response):
    
    def get_channel(self):
        return self.msg[10] << 8 | self.msg[11]
    
    def _can_handle(self, response):
        return response.get_command() == 0x6121
                           
