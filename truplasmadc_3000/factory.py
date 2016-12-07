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

from driver import TruPlasmaDC3000Driver
from protocol import TruPlasmaDC3000Protocol
from e21_util.transport import Serial
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
        return TruPlasmaDC3000Driver(Serial(device, 38400, 8, 'N', 1, 1), protocol)
