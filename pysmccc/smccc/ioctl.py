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
import ctypes
from smccc import common

IOCTLWRITE = 0x1
IOCTLREAD = 0x2

NRBITS = 8
TYPEBITS = 8
SIZEBITS = 14

NRSHIFT = 0
TYPESHIFT = NRSHIFT + NRBITS
SIZESHIFT = TYPESHIFT + TYPEBITS
DIRSHIFT = SIZESHIFT + SIZEBITS


class Smcccreq(ctypes.Structure, common.Printable):
    _pack_ = 1
    _fields_ = [
        ("id", ctypes.c_uint64),
        ("arg0", ctypes.c_uint64),
        ("arg1", ctypes.c_uint64),
        ("arg2", ctypes.c_uint64),
        ]


class Smcccres(ctypes.Structure, common.Printable):
    _pack_ = 1
    _fields_ = [
        ("a0", ctypes.c_int64),
        ("a1", ctypes.c_int64),
        ("a2", ctypes.c_int64),
        ("a3", ctypes.c_int64),
        ]


class Smcccdata(ctypes.Structure, common.Printable):
    _pack_ = 1
    _fields_ = [
        ("req", Smcccreq),
        ("res", Smcccres),
        ]


def IOC(direction, _type, nr, size):
    return (direction << DIRSHIFT) | (_type << TYPESHIFT) | (nr << NRSHIFT) | (size << SIZESHIFT)


def IOWR(_type, nr, size):
    return IOC(IOCTLREAD | IOCTLWRITE, _type, nr, size)


SMCCC_IOCTL_MAGIC = ord("A")
SMCCC_IOCTL_CMD = IOWR(SMCCC_IOCTL_MAGIC, 1, ctypes.sizeof(Smcccdata))
