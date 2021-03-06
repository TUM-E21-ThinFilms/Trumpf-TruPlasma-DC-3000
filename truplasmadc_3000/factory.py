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
from e21_util.log import get_sputter_logger
from e21_util.ports import Ports

class TruPlasmaDC3000Factory:
    
    def get_logger(self):
        return get_sputter_logger('Huettinger TruPlasma 3000/7000', 'huettinger.log')

    def create_sputter(self, device=None, logger=None):
        
        if logger is None:
            logger = self.get_logger()

        if device is None:
            device = Ports().get_port(Ports.DEVICE_SPUTTER_TRUMPF_DC)

        protocol = TruPlasmaDC3000Protocol(0xFFFF, 0x0000, logger)
        return TruPlasmaDC3000Driver(Serial(device, 38400, 8, 'N', 1, 1), protocol)
