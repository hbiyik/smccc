'''
Created on Dec 24, 2024

@author: boogie
'''
import ctypes
from enum import IntEnum

from smccc import common
from smccc import log
from smccc import mem
from smccc.implementations.rockchip import ids
from smccc.implementations.rockchip import sip

MAX_FREQ_COUNT = 6


class DramCommand(IntEnum):
    INIT = 0x00
    SET_RATE = 0x01
    ROUND_RATE = 0x02
    SET_AT_SR = 0x03
    GET_BW = 0x04
    GET_RATE = 0x05
    CLR_IRQ = 0x06
    SET_PARAM = 0x07
    GET_VERSION = 0x08
    POST_SET_RATE = 0x09
    SET_MSCH_RL = 0x0a
    DEBUG = 0x0b
    MCU_START = 0x0c
    ECC = 0x0d
    GET_FREQ_INFO = 0x0e
    ADDRMAP_GET = 0x10
    GET_STALL_TIME = 0x11
    ECC_POISON = 0x12


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
        return self.call(ids.SipCommand.DRAM_CONFIG, arg2=DramCommand.GET_VERSION)

    def shared_mem(self):
        resp = self.request_shared_mem(2, ids.SharedPage.DDR)
        if not resp.status == ids.SipReturn.SUCCESS:
            return
        info = SharedDdr.from_addr(resp.value)
        log.logger.debug(f"DDR Shared Mem: {info}")
        return info

    def dram_freq_info(self):
        return self.call(ids.SipCommand.DRAM_CONFIG, arg0=ids.SharedPage.DDR, arg2=DramCommand.GET_FREQ_INFO)

    def dram_set_rate(self):
        resp = self.call(ids.SipCommand.DRAM_CONFIG, arg0=ids.SharedPage.DDR, arg2=DramCommand.SET_RATE)
        if resp.value in ids.SipReturn:
            resp.value = ids.SipReturn(resp.value)
        return resp

    def dram_mcu_start(self):
        return self.call(ids.SipCommand.DRAM_CONFIG, arg2=DramCommand.MCU_START)

    def dram_mcu_post_set_rate(self):
        return self.call(ids.SipCommand.DRAM_CONFIG, arg0=ids.SharedPage.DDR, arg2=DramCommand.POST_SET_RATE)


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
