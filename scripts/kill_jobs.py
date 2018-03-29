#!/usr/bin/env python

# This script is for killing jobs through PanDA
#

import os
import yaml
import sys
import time
import commands
import json
import subprocess
import random
from termcolor2 import c

import userinterface.Client as Client
from taskbuffer.JobSpec import JobSpec
from taskbuffer.FileSpec import FileSpec


aSrvID = None

#for idx,argv in enumerate(sys.argv):
#    if argv == '-s':
#        aSrvID = sys.argv[idx+1]
#        sys.argv = sys.argv[:idx]
#        break

jobs_to_kill = []
for j in sys.argv[1:]:
    if j.isdigit():
        jobs_to_kill.append(j)

s, o = Client.killJobs(jobs_to_kill, verbose=False )

print("Job killing results:\n=============================")
for i in range(len(jobs_to_kill)):
    if o[i]:
        print(c("%s: %s" % (jobs_to_kill[i], 'success' if o[i] else 'failed')).green)
    else:
        print(c("%s: %s" % (jobs_to_kill[i], 'success' if o[i] else 'failed')).red)
