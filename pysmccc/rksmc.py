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

from smccc.implementations.rockchip import sip
from smccc.implementations.rockchip import ids
from smccc.implementations.rockchip import dmc


with sip.Sip() as rksip:
    print("atf version: ", rksip.atf_version())
    print("sip version: ", rksip.sip_version())
    print("dram version: ", rksip.dram_version())
    phy = rksip.request_shared_mem(2, ids.SharedPage.DDR)
    print("dram config:", dmc.SharedDdr.from_addr(phy))
    print("dram freq info:", rksip.dram_freq_info())
