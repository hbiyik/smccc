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
from smccc.implementations.rockchip import dmc


with sip.RkSip() as rksip:
    print("atf version: ", rksip.atf_version())
    print("sip version: ", rksip.sip_version())

with dmc.Dmc() as rkdmc:
    print("dram version: ", rkdmc.dram_version())
    print("dram config:", rkdmc.shared_mem())
    print("dram freq info:", rkdmc.dram_freq_info())
    print("dram set rate:", rkdmc.dram_set_rate())
    print("dram mcu start:", rkdmc.dram_mcu_start())
