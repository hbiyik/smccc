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
from smccc import mem
from smccc import common


class StatusException(Exception):
    pass


class StatusCode(common.PrettyIntEnum):
    SUCCESS = 0
    NOT_SUPPORTED = -1
    INVALID_PARAMETERS = -2
    DENIED = -3
    NOT_FOUND = -4
    OUT_OF_RANGE = -5
    BUSY = -6
    COMMS_ERROR = -7
    GENERIC_ERROR = -8
    HARDWARE_ERROR = -9
    PROTOCOL_ERROR = -10
    IN_USE = -11


class SharedMem(mem.SharedMem):
    reserved0 = 0
    chan_free = 0
    chan_error = 0
    reserved1 = 0
    reserved2 = 0
    interrupt = 0
    reserved3 = 0
    length = 0
    msgid = 0
    msg_type = 0
    prot_id = 0
    token = 0
    reserved4 = 0
    payload = []

    def __init__(self, start, size):
        mem.SharedMem.__init__(self, start, size)
        self.map(0, 4, "reserved0", encoding="I")
        self.map(4, 4, "chan_free", "chan_error", "reserved1", encoding="I", bitmasks=[(0, 1),
                                                                                       (1, 0),
                                                                                       (2, 30)])
        self.map(8, 8, "reserved2", encoding="Q")
        self.map(16, 4, "interrupt", "reserved3", encoding="I", bitmasks=[(0, 1),
                                                                          (1, 31)])
        self.map(20, 4, "length", encoding="I")
        self.map(24, 4, "msgid", "msg_type", "prot_id", "token", "reserved4", encoding="I", bitmasks=[(0, 8),
                                                                                                      (8, 2),
                                                                                                      (10, 8),
                                                                                                      (18, 10),
                                                                                                      (28, 4)])

    @property
    def payload(self):
        count = max(int(self.length / 4) - 1, 0)
        data = self._f.read(28, count * 4)
        return struct.unpack("i" * count, data)

    @payload.setter
    def payload(self, values):
        if not values:
            return
        if not isinstance(values, tuple) and not isinstance(values, list):
            raise AttributeError("payload must be list or tuple")
        self.length = (len(values) + 1) * 4
        data = struct.pack("I" * len(values), *values)
        self._f.write(28, data)


class Protocol:
    def __init__(self, transport):
        self.transport = transport

    def call(self, functionid, *args):
        response = self.transport.send(self.protocolid, functionid, *args)
        if response[0] < 0:
            raise StatusException(StatusCode(response[0]))
        return response

    def protocol_version(self):
        response = self.call(0)
        return response[1]

    def negotiate_protocol_version(self, version):
        return self.call(0x10, version)

    def protocol_attributes(self):
        response = self.call(0x1)
        payload = response[1]
        num_protocols = common.shiftmask(payload, 0, 8)
        num_agents = common.shiftmask(payload, 8, 8)
        return num_protocols, num_agents

    def protocol_message_attributes(self, msgid):
        response = self.call(0x2, msgid)
        flags = response.playload[1]
        return flags
