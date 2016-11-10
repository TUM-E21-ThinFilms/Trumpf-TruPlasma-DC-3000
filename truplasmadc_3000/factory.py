from driver import TruPlasmaDC3000Driver
from protocol import TruPlasmaDC3000Protocol
from slave.transport import Serial
import logging

class TruPlasmaDC3000Factory:
    
    def get_logger(self):
        logger = logging.getLogger('Huettinger TruPlasma 3000/7000')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('huettinger.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(fh)
        return logger
    
    def create_sputter(self, device="/dev/ttyUSB13", logger=None):
        
        if logger is None:
            logger = self.get_logger()
                    
        protocol = TruPlasmaDC3000Protocol(0xFFFF, 0x0000, logger)
        return TruPlasmaDC3000Driver(Serial(device, 38400, 8, 'N', 1), protocol)
