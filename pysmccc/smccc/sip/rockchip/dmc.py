'''
Created on Dec 24, 2024

@author: boogie
'''
from smccc import common
from smccc import mem
from smccc.sip.rockchip import model
from smccc.sip.rockchip import sip

MAX_FREQ_COUNT = 6


class DramCommand(common.PrettyIntEnum):
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


class SharedDdr(mem.SharedMem, common.Printable):
    hz = 0
    lcdc_type = 0
    sr_idle_en = 0
    addr_mcu_el3 = 0
    wait_flag1 = 0
    wait_flag0 = 0
    complt_hwirq = 0
    update_drv_odt_cfg = 0
    update_deskew_cfg = 0
    freq_count = 0
    freq_info_mhz = []
    wait_mode = 0
    vop_scan_line_time_ns = 0

    def __init__(self, addr):
        _fields_ = [
            ("hz", "I"),
            ("lcdc_type", "I"),
            ("vop", "I"),
            ("vop_dclk_mode", "I"),
            ("sr_idle_en", "I"),
            ("addr_mcu_e13", "I"),
            ("wait_flag1", "I"),
            ("wait_flag0", "I"),
            ("complt_hwirq", "I"),
            ("update_drv_odt_cfg", "I"),
            ("update_deskew_cfg", "I"),
            ("freq_count", "I"),
            (f"freq_info_mhz*{MAX_FREQ_COUNT}", "I" * MAX_FREQ_COUNT),
            ("wait_mode", "I"),
            ("vop_scan_line_time_ns", "I"),
        ]

        size = 0
        for _, dtype in _fields_:
            size += len(dtype) * 4
        super().__init__(addr, size)

        offset = 0
        for name, dtype in _fields_:
            size = len(dtype) * 4
            self.map(offset, size, name, encoding=dtype)
            offset += size


class Dmc(sip.RkSip):
    def dram_version(self):
        return self.call(model.RkSipCommand.DRAM_CONFIG, arg2=DramCommand.GET_VERSION)

    def shared_mem(self):
        resp = self.request_shared_mem(2, model.RkSharedPage.DDR)
        if not resp.status == model.RkSipReturn.SUCCESS:
            return
        info = SharedDdr(resp.value)
        common.logger.debug(f"DDR Shared Mem: {info}")
        return info

    def dram_freq_info(self):
        return self.call(model.RkSipCommand.DRAM_CONFIG,
                         arg0=model.RkSharedPage.DDR, arg2=DramCommand.GET_FREQ_INFO)

    def dram_set_rate(self):
        resp = self.call(model.RkSipCommand.DRAM_CONFIG,
                         arg0=model.RkSharedPage.DDR, arg2=DramCommand.SET_RATE)
        if resp.value in model.RkSipReturn:
            resp.value = model.RkSipReturn(resp.value)
        return resp

    def dram_mcu_start(self):
        return self.call(model.RkSipCommand.DRAM_CONFIG,
                         arg2=DramCommand.MCU_START)

    def dram_mcu_post_set_rate(self):
        return self.call(model.RkSipCommand.DRAM_CONFIG,
                         arg0=model.RkSharedPage.DDR, arg2=DramCommand.POST_SET_RATE)


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

    def applyclock(self, index):
        self.dmc.dram_freq_info()
        self.info.hz = self.info.freq_info_mhz[index] * 1000000
        self.info.wait_flag0 = 1
        self.info.wait_flag1 = 1
        self.info.wait_mode = 1
        resp = self.dmc.dram_set_rate()
        if not resp.status == model.RkSipReturn.SUCCESS:
            common.logger.warning(f"Set rate failed with {resp.status}")
            return resp.status
        self.dmc.dram_mcu_start()
        resp = self.dmc.dram_mcu_post_set_rate()
        if not resp.status == model.RkSipReturn.SUCCESS:
            common.logger.warning(f"Post reset rate failed with {resp.status}")
            return resp.status
        return 0

    def setclock(self, index, mhz):
        self.dmc.dram_freq_info()
        self.info.freq_info_mhz[index] = mhz
        return True
