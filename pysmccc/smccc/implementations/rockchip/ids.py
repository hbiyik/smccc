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
from enum import IntEnum


class SipCommand(IntEnum):
    ATF_VERSION = 0x82000001
    ACCESS_REG = 0x82000002
    SUSPEND_MODE = 0x82000003
    PENDING_CPUS = 0x82000004
    UARTDBG_CFG = 0x82000005
    UARTDBG_CFG64 = 0xc2000005
    MCU_EL3FIQ_CFG = 0x82000006
    ACCESS_CHIP_STATE64 = 0xc2000006
    SECURE_MEM_CONFIG = 0x82000007
    ACCESS_CHIP_EXTRA_STATE64 = 0xc2000007
    DRAM_CONFIG = 0x82000008
    SHARE_MEM = 0x82000009
    SIP_VERSION = 0x8200000a
    REMOTECTL_CFG = 0x8200000b
    PSCI_VPU_RESET = 0x8200000c
    BUS_CFG = 0x8200000d
    LAST_LOG = 0x8200000e
    ACCESS_MEM_OS_REG = 0x8200000f
    SCMI_AGENT0 = 0x82000010
    SCMI_AGENT1 = 0x82000011
    SCMI_AGENT2 = 0x82000012
    SCMI_AGENT3 = 0x82000013
    SCMI_AGENT4 = 0x82000014
    SCMI_AGENT5 = 0x82000015
    SCMI_AGENT6 = 0x82000016
    SCMI_AGENT7 = 0x82000017
    SCMI_AGENT8 = 0x82000018
    SCMI_AGENT9 = 0x82000019
    SCMI_AGENT10 = 0x8200001a
    SCMI_AGENT11 = 0x8200001b
    SCMI_AGENT12 = 0x8200001c
    SCMI_AGENT13 = 0x8200001d
    SCMI_AGENT14 = 0x8200001e
    SCMI_AGENT15 = 0x8200001f
    SDEI_FIQ_DBG_SWITCH_CPU = 0x82000020
    SDEI_FIQ_DBG_GET_EVENT_ID = 0x82000021
    AMP_CFG = 0x82000022
    FIQ_CTRL = 0x82000024
    HDCP_CONFIG = 0x82000025
    WDT_CFG = 0x82000026
    HDMIRX_CFG = 0x82000027
    MCU_CFG = 0x82000028
    PVTPLL_CFG = 0x82000029
    DRAM_FREQ = 0x82000008

    def __str__(self):
        return self.__repr__()


class SharedPage(IntEnum):
    UARTDBG = 1
    DDR = 2
    DDRDBG = 3
    DDRECC = 4
    DDRFSP = 5
    DDRADDRMAP = 6
    LASTLOG = 7
    HDCP = 8
    SLEEP = 9

    def __str__(self):
        return self.__repr__()


class SipReturn(IntEnum):
    SUCCESS = 0
    UNKNOWN = -1
    NOT_SUPPORTED = -2
    INVALID_PARAMS = -3
    INVALID_ADDRESS = -4
    RET_DENIED = -5
    TIMEOUT = -6

    def __str__(self):
        return self.__repr__()
