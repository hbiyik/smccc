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
from smccc import common
from smccc import model


class RkSipCommand(common.PrettyIntEnum):
    ATF_VERSION = model.FunctionId(functionid=1, fast=1, service=model.ServiceCall.SIP)
    DRAM_CONFIG = model.FunctionId(functionid=8, fast=1, service=model.ServiceCall.SIP)
    SHARE_MEM = model.FunctionId(functionid=9, fast=1, service=model.ServiceCall.SIP)
    SIP_VERSION = model.FunctionId(functionid=10, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT0 = model.FunctionId(functionid=16, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT1 = model.FunctionId(functionid=17, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT2 = model.FunctionId(functionid=18, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT3 = model.FunctionId(functionid=19, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT4 = model.FunctionId(functionid=20, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT5 = model.FunctionId(functionid=21, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT6 = model.FunctionId(functionid=22, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT7 = model.FunctionId(functionid=23, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT8 = model.FunctionId(functionid=24, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT9 = model.FunctionId(functionid=25, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT10 = model.FunctionId(functionid=26, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT11 = model.FunctionId(functionid=27, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT12 = model.FunctionId(functionid=28, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT13 = model.FunctionId(functionid=29, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT14 = model.FunctionId(functionid=30, fast=1, service=model.ServiceCall.SIP)
    SCMI_AGENT15 = model.FunctionId(functionid=31, fast=1, service=model.ServiceCall.SIP)


class RkSharedPage(common.PrettyIntEnum):
    UARTDBG = 1
    DDR = 2
    DDRDBG = 3
    DDRECC = 4
    DDRFSP = 5
    DDRADDRMAP = 6
    LASTLOG = 7
    HDCP = 8
    SLEEP = 9


class RkSipReturn(common.PrettyIntEnum):
    SUCCESS = 0
    UNKNOWN = -1
    NOT_SUPPORTED = -2
    INVALID_PARAMS = -3
    INVALID_ADDRESS = -4
    RET_DENIED = -5
    TIMEOUT = -6
