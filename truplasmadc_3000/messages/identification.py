from truplasmadc_3000.message import Message, Response, hex_to_float, float_to_hex

class IdentificationMessage(Message):
    def __init__(self):
        self.do_allocate(10)
        self.set_command(0x6101)
        
    def response_length(self):
        return 32
    
    def create_response(self, bytes):
        return IdentificationResponse(bytes)
        
class IdentificationResponse(Response):
    
    def get_identification(self):
        return self.msg[8] << 8 | self.msg[9]
    
    def is_dc_plus(self):
        return self.get_identification() == 0x6804
    
    def is_dc_normal(self):
        return self.get_identification() == 0x6802
    
    def get_device_type(self):
        return "".join(map(chr, self.msg[10:29]))
    
    def _can_handle(self, response):
        return response.get_command() == 0x6101
                           
