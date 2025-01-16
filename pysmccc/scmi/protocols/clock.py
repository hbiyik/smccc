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


class AttrRateFlags(block.MappedBlock, common.Printable):
    numrates = 0
    return_triplet = 0
    remaining = 0

    def __init__(self, buf):
        block.MappedBlock.__init__(self, buf)
        self.map(0, 4, "numrates", "return_triplet", "_reserved0", "remaining",
                 encoding="I", bitmasks=[(0, 12),
                                         (12, 1),
                                         (13, 3),
                                         (16, 16)
                                         ])


class SetRateFlags(block.MappedBlock, common.Printable):
    asynch = 0
    ignore_asynch = 0
    roundup = 0

    def __init__(self, buf):
        block.MappedBlock.__init__(self, buf)
        self.map(0, 4, "asynch", "ignore_asynch", "roundup", "_reserved0",
                 encoding="I", bitmasks=[(0, 1),
                                         (1, 1),
                                         (2, 2),
                                         (4, 28)
                                         ])

    def __int__(self):
        self._f.seek(0)
        return struct.unpack("I", self._f.read(4))[0]


class Clock(model.Protocol):
    protocolid = model.Protocols.CLOCK_MANAGEMENT

    def attributes(self, clockid):
        response = self.call(0x3, clockid)
        return ClockAttributes(struct.pack("I", response[1]))

    def describe_rates(self, clockid, rateindex):
        response = self.call(0x4, clockid, rateindex)
        flags = AttrRateFlags(struct.pack("I", response[1]))
        clocks = []
        index = 0
        record = 0
        while record < flags.numrates:
            if flags.return_triplet:
                fmin = common.uint32_cast("Q", response[index + 2], response[index + 3])
                fmax = common.uint32_cast("Q", response[index + 4], response[index + 5])
                fstep = common.uint32_cast("Q", response[index + 6], response[index + 7])
                subclocks = list(range(fmin, fmax + fstep, fstep))
                clocks.extend(subclocks)
                index += 6
            else:
                clocks.append(common.uint32_cast("Q", response[index + 2], response[index + 3]))
                index += 2
            record += 1
        return clocks

    def rateset(self, clockid, rate, asynch=0, ignore_asynch=0, roundmode=0):
        flags = SetRateFlags(b"0000")
        flags.asynch = asynch
        flags.ignore_asynch = ignore_asynch
        flags.roundup = roundmode
        rate_high = common.shiftmask(rate, 32, 32)
        rate_low = common.shiftmask(rate, 0, 32)
        self.call(0x5, int(flags), clockid, rate_low, rate_high)

    def rateget(self, clockid):
        response = self.call(0x6, clockid)
        return common.uint32_cast("Q", response[1], response[2])
