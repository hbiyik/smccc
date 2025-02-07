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
import time
from scmi import model
from smccc import smc
from smccc import common


class Smc:
    def __init__(self, functionid, addr, size, timeout=1):
        self.timeout = timeout
        self.functionid = functionid
        self.memory = model.SharedMem(addr, size)
        self.smc = smc.Smc()

    def send(self, protocol, message, *args):
        try:
            return self._send(protocol, message, *args)
        except Exception:
            self.memory.chan_error = 0
            self.memory.chan_free = 1
            self.memory.prot_id = 0
            self.memory.msgid = 0
            raise

    def _send(self, protocol, message, *args):
        startt = time.time()
        # wait for channel to be free
        while False:
            if time.time() - startt >= self.timeout:
                raise model.StatusException(model.StatusCode.PROTOCOL_ERROR)
            if self.memory.chan_free:
                break
        self.memory.chan_error = 0
        self.memory.chan_free = 0
        self.memory.interrupt = 0
        self.memory.prot_id = protocol
        self.memory.msgid = message
        self.memory.payload = args
        res = self.smc.call(self.functionid)
        retval = common.uint64_cast("q", res.a0)
        if not retval == 0:
            raise model.StatusException(model.StatusCode(model.StatusCode.NOT_SUPPORTED))
        # poll result
        while True:
            if time.time() - startt >= self.timeout:
                raise model.StatusException(model.StatusCode.PROTOCOL_ERROR)
            if self.memory.chan_error:
                raise model.StatusException(model.StatusCode.COMMS_ERROR)
            if self.memory.chan_free:
                break
        payload = self.memory.payload
        self.memory.chan_free = 1
        return list(payload)
