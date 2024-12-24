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
import array
import os
import mmap
import binascii
import ctypes
from smccc import common


class Io:
    def __init__(self, start, size, dev="/dev/mem", pagesize=4096, read=True, write=True):
        self.flag_r = read
        self.flag_w = write
        self.dev = dev
        self.pagesize = pagesize
        self.start = start
        self.size = size
        self.isinited = False

    def init(self):
        self.isinited = True

    def read(self, start, size):
        if not self.isinited:
            self.init()
        return self.readio(start, size)

    def write(self, start, data):
        if not self.isinited:
            self.init()
        return self.writeio(start, data)

    def close(self):
        pass

    def writeio(self, start, size, data):
        raise NotImplementedError

    def readio(self, start, size):
        raise NotImplementedError


class Memory(Io):
    def init(self):
        # PAGESIZE ALIGN
        if os.path.exists("/dev/insecure_mem"):
            self.dev = "/dev/insecure_mem"
        self.startoffset = self.start % self.pagesize
        start = int(self.start / self.pagesize) * self.pagesize
        startoffset = self.start - start
        size = (int((self.size + startoffset) / self.pagesize) + 1) * self.pagesize
        common.logger.debug("%s binding: [%d (%s), %d (%s)]", self.dev, start, hex(start), start + size, hex(start + size))
        # MAP physical memory
        if self.flag_r and self.flag_w:
            flags = os.O_RDWR | os.O_SYNC
        else:
            flags = os.O_RDONLY | os.O_CLOEXEC
        self.f = os.open(self.dev, flags)
        flags = 0
        if self.flag_r:
            flags |= mmap.PROT_READ
        if self.flag_w:
            flags |= mmap.PROT_WRITE
        self.mmap = mmap.mmap(self.f, size, mmap.MAP_SHARED, flags, offset=start)
        self.bindstart = start
        self.bindsize = size
        super(Memory, self).init()

    def readio(self, start, size):
        self.mmap.seek(self.startoffset + start)
        val = self.mmap.read(size)
        common.logger.debug("%s read start: %s, size: %d, val: 0x%s", self.dev, hex(self.start + self.startoffset + start), size, binascii.hexlify(val).decode())
        return val

    def writeio(self, start, data):
        common.logger.debug("%s write start: %s data: 0x%s", self.dev, hex(self.start + self.startoffset + start), binascii.hexlify(data).decode())
        self.mmap.seek(self.startoffset + start)
        retval = self.mmap.write(data)
        common.logger.debug("%s is written with %d length", self.dev, retval)
        return retval

    def close(self):
        if self.isinited:
            common.logger.debug("%s unbinding: [%d (%s), %d (%s)]", self.dev,
                                self.bindstart, hex(self.bindstart),
                                self.bindsize, hex(self.bindsize))
            self.mmap.close()
            os.close(self.f)


class MmapStructure(ctypes.Structure):
    @classmethod
    def from_addr(cls, addr):
        mem = Memory(addr, ctypes.sizeof(cls))
        obj = cls.from_buffer_copy(mem.read(0, ctypes.sizeof(cls)))
        obj._memory = mem
        obj._attrlist = [x[0] for x in obj._fields_]
        obj._buffer = obj.__buffer__(0).cast("B")
        return obj

    def __isctype(self, name):
        return hasattr(self, "_memory") and not name.startswith("_") and name in self._attrlist

    def __setattr__(self, name, value):
        ctypes.Structure.__setattr__(self, name, value)
        if not self.__isctype(name):
            return
        attr = getattr(self.__class__, name)
        self._memory.write(attr.offset, self._buffer[attr.offset: attr.offset + attr.size])

    def __getattr__(self, name):
        if not self.__isctype(name):
            return ctypes.Structure.__getattr__(self, name)
        attr = getattr(self.__class__, name)
        self._buffer[attr.offset: attr.offset + attr.size] = self._memory.read(attr.offset, attr.size)
        return ctypes.Structure.__getattr__(self, name)
