'''
Created on Dec 24, 2024

@author: boogie
'''
import ctypes

from smccc import common
from smccc import mem

MAX_FREQ_COUNT = 6


class SharedDdr(mem.MmapStructure, common.Printable):
    _pack_ = 1
    _fields_ = [
        ("hz", ctypes.c_uint32),
        ("lcdc_type", ctypes.c_uint32),
        ("vop", ctypes.c_uint32),
        ("vop_dclk_mode", ctypes.c_uint32),
        ("sr_idle_en", ctypes.c_uint32),
        ("addr_mcu_e13", ctypes.c_uint32),
        ("wait_flag1", ctypes.c_uint32),
        ("wait_flag0", ctypes.c_uint32),
        ("complt_hwirq", ctypes.c_uint32),
        ("update_drv_odt_cfg", ctypes.c_uint32),
        ("update_deskew_cfg", ctypes.c_uint32),
        ("freq_count", ctypes.c_uint32),
        ("freq_info_mhz", ctypes.c_uint32 * MAX_FREQ_COUNT),
        ("wait_mode", ctypes.c_uint32),
        ("vop_scan_line_time_ns", ctypes.c_uint32),
        ]
