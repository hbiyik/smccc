'''
Created on Dec 24, 2024

@author: boogie
'''
import ctypes
import time

from smccc import common
from smccc import log
from smccc import mem
from smccc.implementations.rockchip import ids
from smccc.implementations.rockchip import sip

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


class Dmc(sip.Sip):
    def dram_version(self):
        return self.call(ids.DRAM_CONFIG, arg2=ids.CONFIG_DRAM_GET_VERSION)

    def shared_mem(self):
        resp = self.request_shared_mem(2, ids.SharedPage.DDR)
        if not resp.status == ids.SipReturn.SUCCESS:
            return
        info = SharedDdr.from_addr(resp.value)
        log.logger.debug(f"DDR Shared Mem: {info}")
        return info

    def dram_freq_info(self):
        return self.call(ids.DRAM_CONFIG, arg0=ids.SharedPage.DDR, arg2=ids.CONFIG_DRAM_GET_FREQ_INFO)

    def dram_set_rate(self):
        resp = self.call(ids.DRAM_CONFIG, arg0=ids.SharedPage.DDR, arg2=ids.CONFIG_DRAM_SET_RATE)
        if resp.value in ids.SipReturn:
            resp.value = ids.SipReturn(resp.value)
        return resp

    def dram_mcu_start(self):
        return self.call(ids.DRAM_CONFIG, arg2=ids.CONFIG_MCU_START)

    def dram_mcu_post_set_rate(self):
        return self.call(ids.DRAM_CONFIG, arg0=ids.SharedPage.DDR, arg2=ids.CONFIG_DRAM_POST_SET_RATE)


class Dram:
    def __init__(self):
        self.dmc = Dmc()
        self.info = self.dmc.shared_mem()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dmc.close()

    def getclocks(self):
        self.dmc.dram_freq_info()
        return list(self.info.freq_info_mhz)

    def setclock(self, mhz):
        self.dmc.dram_freq_info()
        self.info.hz = mhz * 1000000
        self.info.wait_flag0 = 0
        self.info.wait_flag1 = 0
        self.info.wait_mode = 1
        resp = self.dmc.dram_set_rate()
        if not resp.status == ids.SipReturn.SUCCESS:
            log.logger.warning(f"Set rate failed with {resp.status}")
            return resp.status
        self.dmc.dram_mcu_start()
        resp = self.dmc.dram_mcu_post_set_rate()
        if not resp.status == ids.SipReturn.SUCCESS:
            log.logger.warning(f"Post reset rate failed with {resp.status}")
            return resp.status
        return 0
