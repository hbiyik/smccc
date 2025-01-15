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
from smccc import block
from smccc import common


class ClockAttributes(block.MappedBlock, common.Printable):
    enabled = 0
    restricted = 0
    _reserved0 = 0
    extended = 0
    parent = 0
    extended_name = 0
    rate_change_request = 0
    rate_change_support = 0

    def __init__(self, block):
        block.MappedBlock.__init__(self, block)
        self.map(0, 4, "enabled", "restricted", "_reserved0", "extended", "parent", "extended_name", "rate_change_request", "range_check_support",
                 encoding="I", bitmasks=[(0, 1),
                                         (1, 1),
                                         (2, 25),
                                         (27, 1),
                                         (28, 1),
                                         (29, 1),
                                         (30, 1),
                                         (31, 1),
                                         ])


class RateFlags(block.MappedBlock, common.Printable):
    numrates = 0
    return_triplet = 0
    remaining = 0

    def __init__(self, block):
        block.MappedBlock.__init__(self, block)
        self.map(0, 4, "numrates", "return_triplet", "_reserved0", "remaining",
                 encoding="I", bitmasks=[(0, 12),
                                         (12, 1),
                                         (13, 3),
                                         (16, 16)
                                         ])


class Clock(model.Protocol):
    protocolid = model.Protocols.CLOCK_MANAGEMENT

    def attributes(self, clockid):
        response = self.call(0x3, clockid)
        return ClockAttributes(struct.pack("I", response[1]))

    def describe_rates(self, clockid, rateindex):
        response = self.call(0x4, clockid, rateindex)
        flags = RateFlags(struct.pack("I", response[1]))
        clocks = []
        index = 0
        while index < flags.numrates:
            if flags.return_triplet:
                fmin = response[index + 2]
                fmax = response[index + 3]
                fstep = response[index + 4]
                subclocks = list(range(fmin, fmax + fstep, fstep))
                clocks.extend(subclocks)
                index += 3
            else:
                clocks.append(response[index + 3], response[index + 2])
                index += 2
        return clocks
