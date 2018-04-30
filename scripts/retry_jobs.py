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

if len(sys.argv)==1:
    print("No joID given")
    sys.exit(1)

jobs_to_retry = sys.argv[1]

s, o = Client.retryJob(jobs_to_retry, verbose=True)

print s

print("Job retry results:\n=============================")
for i in range(len(jobs_to_kill)):
    if o[i]:
        print(c("%s: %s" % (jobs_to_kill[i], 'success' if o[i] else 'failed')).green)
    else:
        print(c("%s: %s" % (jobs_to_kill[i], 'success' if o[i] else 'failed')).red)
