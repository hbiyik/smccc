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
from smccc import common
from smccc import log
from smccc.implementations.rockchip import ids
import ctypes


class Response(common.Printable):
    def __init__(self, ret):
        self._ret = ret
        self.status = ctypes.c_int64(ret.a0).value
        if self.status in ids.SipReturn:
            self.status = ids.SipReturn(self.status)
        self._a1 = ret.a1
        self._a2 = ret.a2
        self._a3 = ret.a3
        self.value = ctypes.c_int32(ret.a1).value
        log.logger.debug(self)


class Sip(smc.Smc):
    def call(self, functionid, **kwargs):
        log.logger.debug(f"Request: {functionid} {kwargs}")
        return Response(smc.Smc.call(self, functionid, **kwargs))

    def atf_version(self):
        return self.call(ids.ATF_VERSION)

    def sip_version(self):
        return self.call(ids.SIP_VERSION)

    def request_shared_mem(self, count, memtype):
        return self.call(ids.SHARE_MEM, arg0=count, arg1=memtype)
