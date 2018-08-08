#!/usr/bin/env python

# This script is for quering job state through PanDA
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

jobs_to_query = []
for j in sys.argv[1:]:
    if j.isdigit():
        jobs_to_query.append(j)

o = Client.getJobStatus(jobs_to_query)

for j in o[1]:
    if j is None:
        continue
    message_template = "%s: %s (%s): %s %s" % (j.PandaID, j.jobStatus, j.jobSubStatus, j.jobParameters, j.cmtConfig)
    message = None
    if j.jobStatus=='finished':
        message = c(message_template).green
    elif j.jobStatus=='failed':
        message = c(message_template).red
    elif j.jobStatus=='running' or j.jobStatus=='starting' or j.jobStatus=='transferring':
        message = c(message_template).blue
    elif j.jobStatus=='sent' or j.jobStatus=='holding':
        message = c(message_template).yellow
    elif j.jobStatus=='cancelled':
        message = c(message_template).cyan
    elif j.jobStatus=='defined':
        message = c(message_template).cyan
    elif j.jobStatus=='activated':
        message = c(message_template).cyan
    else: # unknown
        message = '%s: job does not exist or status=%s' % (j.PandaID, j.jobStatus)
    print(message)
    print
