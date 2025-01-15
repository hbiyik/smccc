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
from scmi import model


class Base(model.Protocol):
    protocolid = model.Protocols.BASE

    def discover_vendor(self):
        response = self.call(0x3)
        vendorid = struct.pack("c" * 16,
                               response[1],
                               response[2],
                               response[3],
                               response[4])
        return vendorid

    def discover_subvendor(self):
        response = self.call(0x4)
        vendorid = struct.pack("c" * 16,
                               response[1],
                               response[2],
                               response[3],
                               response[4])
        return vendorid

    def discover_implementation_version(self):
        response = self.call(0x5)
        return response[1]

    def discover_list_protocols(self, skip=0):
        response = self.call(0x6, skip)
        protocols = []
        num_protocols = response[1]
        for index in range(int(num_protocols / 4) + 1):
            for protocol in struct.unpack("BBBB", struct.pack("I", response[index + 2])):
                if not len(protocols) == num_protocols:
                    protocols.append(model.Protocols(protocol))
        return protocols

    def discover_agent(self):
        response = self.call(0x7)
        agentid = response[1]
        agentname = struct.pack("c" * 16,
                                response[2],
                                response[3],
                                response[4],
                                response[5])
        return agentid, agentname

    def notify_errors(self, enable):
        self.call(0x8, int(bool(enable)))

    def set_device_permissions(self, agentid, deviceid, allow):
        self.call(0x9, agentid, deviceid, int(bool(allow)))

    def set_protocol_permissions(self, agentid, deviceid, protocolid, allow):
        self.call(0x10, agentid, deviceid, protocolid, int(bool(allow)))

    def reset_agent_configuration(self, agentid, reset):
        self.call(0x11, agentid, int(bool(reset)))

    def error_event(self, agentid, error_status):
        pass
