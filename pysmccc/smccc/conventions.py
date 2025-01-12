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
from smccc import common


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


class FunctionID:
    fast = 0
    smc64 = 0
    _service = 0
    mustbezero = 0
    nolivestate = 0
    function = 0

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        self._service = ServiceCall(value)

    def __init__(self, val=None):
        if val is not None:
            self.fast = common.shiftmask(val, 31, 1)
            self.smc64 = common.shiftmask(val, 30, 1)
            self.service = common.shiftmask(val, 24, 6)
            self.mustbezero = common.shiftmask(val, 17, 7)
            self.nolivestate = common.shiftmask(val, 16, 1)
            self.function = common.shiftmask(val, 0, 16)

    def __int__(self):
        return common.maskshift(self.fast, 1, 31) | \
            common.maskshift(self.smc64, 1, 30) | \
            common.maskshift(self.service, 6, 24) | \
            common.maskshift(self.mustbezero, 7, 17) | \
            common.maskshift(self.nolivestate, 1, 16) | \
            common.maskshift(self.function, 16, 0)

    def __repr__(self):
        return f"0x{int(self):08X}"
