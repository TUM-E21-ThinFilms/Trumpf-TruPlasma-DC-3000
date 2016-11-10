from slave.protocol import Protocol
from message import Message, Response

class CommunicationError(Exception):
    pass

class TruPlasmaDC3000Protocol(Protocol):
    def __init__(self, receiver=0xFFFF, sender=0x0000, logger=None):

        self.logger = logger
        self.receiver = receiver
        self.sender = sender

    def set_logger(self, logger):
        self.logger = logger

    def set_name(self, name):
        self.name = name

    def send_message(self, transport, message):

        message.set_source(self.sender)
        message.set_destination(self.receiver)

        message.finish()
        data = message.to_binary()
        self.logger.debug('Sendign: "%s"', message)

        transport.write(data)
        
    def query(self, transport, message):
        
        self.send_message(transport, message)
        
        length = message.response_length()
        raw_response = transport.read_bytes(length)
        
        self.logger.debug('Recevied response (%s bytes): "%s"', str(length), " ".join(map(hex, raw_response)))
       
        response_as_hex = []
        
        for i in range(0, length):
            response_as_hex.append(raw_response[i])
        
        response = message.create_response(response_as_hex)
        
        if not response.is_valid_crc():
            raise CommunicationError('Received an invalid response packet. CRC dismatch.')
        
        if response.is_nack():
            self.logger.warning('Received a NAK Response')
         
        return response

    def write(self, transport, message):
        return self.query(transport, message)