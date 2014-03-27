#!/usr/bin/env python

import sys
import os

cfgfile = open("/etc/skarphed/skarphed.conf","r")
cfgdata = cfgfile.read().split("\n")
cfgfile.close()
cfg = {}
for line in cfgdata:
    if line.startswith("#") or line.find("=") == -1:
        continue
    key, value = line.split("=")
    cfg[key]=value

sys.path.append(os.path.dirname(__file__))

from instanceconf import SCV_INSTANCE_SCOPE_ID
cfg["SCV_INSTANCE_SCOPE_ID"] = SCV_INSTANCE_SCOPE_ID

from skarphedcore.scv import Core
from skarphedcore.scv import OperationDaemon

core = Core(cfg)
configuration = core.get_configuration()
pidfile = configuration.get_entry("core.webpath")+"/opd.pid"
opd = OperationDaemon(core, pidfile)

# This script accepts a dummy argument (sys.argv[2])
# This argument is supposed to be the instance id, so
# one can distinguish the daemon-processes from each 
# other in e.g. htop

success = False
if len(sys.argv) == 2 or len(sys.argv) == 3:
    if sys.argv[1] == 'start':
        opd.start()
        success = True
    elif sys.argv[1] == 'stop':
        opd.stop()
        success = True
    elif sys.argv[1] == 'restart':
        opd.restart()
        success = True
    elif sys.argv[1] == 'status':
        if os.path.exists(pidfile):
          print 0
          sys.exit(0)
        else:
          print 1
          sys.exit(1)

if not success:
    print """
          Skarphed OperationDaemon
          ========================

          Options: start, stop, restart

          Example:

          python operation_daemon.py start
          python operation_daemon.py stop
          python operation_daemon.py restart
          """

