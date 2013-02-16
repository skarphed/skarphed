#!/usr/bin/env python

import sys
import os

cfgfile = open("/etc/scoville/scoville.conf","r").read().split("\n")
cfg = {}
for line in cfgfile:
    if line.startswith("#") or line.find("=") == -1:
        continue
    key, value = line.split("=")
    cfg[key]=value

del(cfgfile)

p = os.path.realpath(__file__)
p = p.replace("scoville.pyc","")
p = p.replace("scoville.py","")
sys.path.append(p)

from instanceconf import SCV_INSTANCE_SCOPE_ID
cfg["SCV_INSTANCE_SCOPE_ID"] = SCV_INSTANCE_SCOPE_ID

sys.path.append(cfg["SCV_LIBPATH"])

from scv import Core

core = Core(cfg)
OperationDaemon = core.get_operation_manager.get_operation_daemon()
pidfile = "/tmp/scv_opd_"+str(cfg["SCV_INSTANCE_SCOPE_ID"])+".pid"
opd = OperationDaemon(core, pidfile)

success = False
if len(sys.argv) == 2:
    if sys.argv[1] == 'start':
        opd.start()
        success = True
    elif sys.argv[1] == 'stop':
        opd.stop()
        success = True
    elif sys.argv[1] == 'restart':
        opd.restart()
        success = True

if not success:
    print """
          Scoville OperationDaemon
          ========================

          Options: start, stop, restart

          Example:

          python operation_daemon.py start
          python operation_daemon.py stop
          python operation_daemon.py restart
          """

