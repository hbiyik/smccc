"""
 Copyright (C) 2025 boogie

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
import struct
from smccc import common
from smccc import block


class ServiceCall(common.PrettyIntEnum):
    ARM_ARCH = 0
    CPU = 1
    SIP = 2
    OEM = 3
    STD_SECURE = 4
    STD_HYPERVISOR = 5
    VENDOR_HYPERVISOR = 6
    VENDOR_EL3_MONITOR = 7
    # 8 - 47: reserved
    TRUSTES_APP_0 = 48
    TRUSTES_APP_1 = 49
    # 50 - 53: Trusted OS


class FunctionId(block.MappedBlock, common.Printable):
    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        if not isinstance(value, ServiceCall):
            value = ServiceCall(value)
        self._service = value

    def __init__(self, fast=0, smc64=0, service=0, _reserved0=0, nolivestate=0, functionid=0):
        block.MappedBlock.__init__(self, b"0000")
        self.map(0, 4, "functionid", "nolivestate", "_reserved0", "_service", "smc64", "fast", encoding="I",
                 bitmasks=[(0, 16),
                           (16, 1),
                           (17, 7),
                           (24, 6),
                           (30, 1),
                           (31, 1)])
        self.functionid = functionid
        self.nolivestate = nolivestate
        self._reserved0 = _reserved0
        self._service = service
        self.smc64 = smc64
        self.fast = fast

    def __int__(self):
        self._f.seek(0)
        return struct.unpack("I", self._f.read(4))[0]
