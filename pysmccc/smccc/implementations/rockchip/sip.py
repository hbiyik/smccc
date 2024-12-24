"""
 Copyright (C) 2024 boogie

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from smccc import smc
from smccc.implementations.rockchip import ids


class Sip(smc.Smc):
    def atf_version(self):
        return self.call(ids.ATF_VERSION)

    def sip_version(self):
        return self.call(ids.SIP_VERSION).a1

    def dram_version(self):
        return self.call(ids.DRAM_CONFIG, arg2=ids.CONFIG_DRAM_GET_VERSION).a1

    def request_shared_mem(self, count, memtype):
        return self.call(ids.SHARE_MEM, arg0=count, arg1=memtype).a1

    def dram_freq_info(self):
        return self.call(ids.SHARE_MEM, arg1=ids.CONFIG_DRAM_GET_FREQ_INFO)
