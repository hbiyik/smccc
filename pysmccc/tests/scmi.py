'''
Created on Jan 12, 2025

@author: boogie
'''
REMOTE_DBG = "192.168.2.10"

if REMOTE_DBG:
    import pydevd  # @UnresolvedImport
    pydevd.settrace(REMOTE_DBG, stdoutToServer=True, stderrToServer=True, suspend=False)

from scmi.transports import smc
from scmi.protocols import base

SCMI_AGENT1 = 0x82000010
t = smc.Smc(SCMI_AGENT1, 0x10f000, 0x100)
b = base.Base(t)
print("procotols", b.discover_list_protocols(0))
