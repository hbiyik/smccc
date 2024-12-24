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
import fcntl
import ctypes
import array

from smccc import ioctl
from smccc import common


class Smc:
    def __init__(self):
        self.fd = open(common.PROCPATH, "wb")

    def close(self):
        self.fd.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def call(self, functionid, **kwargs):
        buf = array.array("B", [0] * ctypes.sizeof(ioctl.Smcccdata))
        data = ioctl.Smcccdata.from_buffer(buf)
        data.req.id = functionid
        data.req.arg0 = kwargs.get("arg0", 0)
        data.req.arg1 = kwargs.get("arg1", 0)
        data.req.arg2 = kwargs.get("arg2", 0)
        fcntl.ioctl(self.fd.fileno(), ioctl.SMCCC_IOCTL_CMD, data)
        return data.res
