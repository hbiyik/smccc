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

import os
import mmap
import binascii
from smccc import common
from smccc import block


class Memory:
    def __init__(self, start, size, dev="/dev/mem", pagesize=4096, read=True, write=True):
        self.flag_r = read
        self.flag_w = write
        self.dev = dev
        self.pagesize = pagesize
        self._start = start
        self.size = size
        self.length = size
        self.isinited = False
        # PAGESIZE ALIGN
        if os.path.exists("/dev/insecure_mem"):
            self.dev = "/dev/insecure_mem"
        self.startoffset = self._start % self.pagesize
        start = int(self._start / self.pagesize) * self.pagesize
        startoffset = self._start - start
        size = (int((self.size + startoffset) / self.pagesize) + 1) * self.pagesize
        common.logger.debug("%s binding: [%d (%s), %d (%s)]", self.dev, start, hex(start), start + size, hex(start + size))
        # MAP physical memory
        if self.flag_r and self.flag_w:
            flags = os.O_RDWR | os.O_SYNC
        else:
            flags = os.O_RDONLY | os.O_CLOEXEC
        self._f = os.open(self.dev, flags)
        flags = 0
        if self.flag_r:
            flags |= mmap.PROT_READ
        if self.flag_w:
            flags |= mmap.PROT_WRITE
        self.mmap = mmap.mmap(self._f, size, mmap.MAP_SHARED, flags, offset=start)
        self.bindstart = start
        self.length = size

    def seek(self, pos):
        common.logger.debug("%s seek: %s", self.dev, hex(self._start + self.startoffset + pos))
        return self.mmap.seek(self.startoffset + pos)

    def read(self, size):
        val = b""
        for _ in range(size):
            val += self.mmap.read(1)
        common.logger.debug("%s read: size: %d, val: 0x%s", self.dev, size, binascii.hexlify(val).decode())
        return val

    def write(self, data):
        common.logger.debug("%s write: 0x%s", self.dev, binascii.hexlify(data).decode())
        retval = self.mmap.write(data)
        common.logger.debug("%s is written with length %d", self.dev, retval)
        return retval

    def close(self):
        if self.isinited:
            common.logger.debug("%s unbinding: [%d (%s), %d (%s)]", self.dev,
                                self.bindstart, hex(self.bindstart),
                                self.length, hex(self.length))
            self.mmap.close()
            os.close(self._f)


class SharedMem(block.MappedBlock):
    def __init__(self, start, size):
        self._map = []
        self._attrs = {}
        self._f = Memory(start, size)
