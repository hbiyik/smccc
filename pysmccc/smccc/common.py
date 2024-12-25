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
from enum import IntEnum

PROCPATH = "/proc/smccc"


class Printable:
    def __repr__(self):
        attrs = [(k, v) for (k, v) in self.__dict__.items() if not k.startswith("_")]
        if hasattr(self, "_fields_"):
            for k, v in self._fields_:
                if k.startswith("_"):
                    continue
                val = getattr(self, k)
                if isinstance(val, ctypes.Array):
                    val = list(val)
                attrs += [(k, val)]
        return f"{self.__class__.__name__}: " + ", ".join([f"{k}={repr(v)}" for (k, v) in attrs])
