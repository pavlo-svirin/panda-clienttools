#!/usr/bin/env python2

import os.path
import sys
from jinja2 import Template, Environment, FileSystemLoader, StrictUndefined, DebugUndefined, meta
import ast
import re
import yaml
import numpy as np
from termcolor2 import c
import random
import string

#RANGE_RE = "\[(\d+):(\d+)(:(\d+))?\]"
RANGE_RE = '\[(\-?\d+(\.\d+)?):(\-?\d+(\.\d+)?)(:(\-?\d+(\.\d+)?))?\]'
range_re = re.compile(RANGE_RE)

if len(sys.argv)==1:
    print("Please specify a template")
    sys.exit(1)

# also read walltime & nodes count    

template_file = sys.argv[1]

if not os.path.exists(template_file):
    print("Template does not exist")
    sys.exit(2)

THIS_DIR = os.path.dirname(os.path.abspath(template_file))

# read template
template_data = None
with open(template_file, 'r') as stream:
    try:
        template_data = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(3)

# sort variables
# print(template_data['variables']) 
literals = {}
arrays = {}
vars_used = set()

dst_output = {}


#filename  = ''
#if 'filename' in template_data:
#    filename = template_data['filename']

env = Environment()
#templateLoader = FileSystemLoader(THIS_DIR)
#env = Environment(loader=templateLoader)

#tmpl = env.parse(template_data['jobs'])

expected_vars = set()

jobs = template_data['jobs']
sequence = template_data['sequence']

for j,k in template_data['jobs'].iteritems():
    tmpl = env.parse(j)
    expected_vars.update(meta.find_undeclared_variables(tmpl))
    tmpl = env.parse(k['command'])
    expected_vars.update(meta.find_undeclared_variables(tmpl))


for j,k in template_data['sequence'].iteritems():
    tmpl = env.parse(j)
    expected_vars.update(meta.find_undeclared_variables(tmpl))
    tmpl = env.parse(k)
    expected_vars.update(meta.find_undeclared_variables(tmpl))

#print(expected_vars)


#tmpl = env.get_template(filename)
#tmpl = env.parse(filename)
#expected_vars = meta.find_undeclared_variables(tmpl)

#print expected_vars
#print tmpl.render(wf_no=1)
#sys.exit(0)

#queuename = ''
#if 'queuename' in template_data:
#    queuename = template_data['queuename']

#walltime =''
#if 'walltime' in template_data:
#    walltime = template_data['walltime']

#name  =''
#if 'name' in template_data:
#    name = template_data['name']

for k,v in template_data['variables'].iteritems():
    if k in expected_vars:
        # read variables list
        try:
            x = ast.literal_eval(v)
            if isinstance(x, list) and any(x):
                if any(x):
                    if len(x)==1:
                        literals[k] = x[0]
                    else:
                        #arrays[k] = "[%s]" % (",".join(x))
                        arrays[k] = x
                else:
                    print(c("Ignoring empty  declaration of %s" % v).magenta)
            else:
                #literals[k] = x
                literals[k] = [x]
            vars_used.add(k)
        except SyntaxError:
            range_match = re.search(range_re, v)
            if range_match is None: # it's a string anyway
                literals[k] = v
                vars_used.add(k)
                continue
            seq_data = list(range_match.groups())
            step = seq_data[5]
            seq_data = [seq_data[0], seq_data[2]]
            if step is not None: # no step given
                seq_data.append(step)
            # identifying range vars type
            f = int
            for s in seq_data:
                if s.find('.') <> -1:
                    f = float
                    break
            seq_data = map(f, seq_data)
            arr = np.arange(seq_data[0], seq_data[1], *seq_data[2:])
            if any(arr):
                if len(arr) == 1:
                    literals[k] = arr[0]
                else:
                    #arrays[k] = "[%s]" % ",".join(str(a) for a in arr)
                    arrays[k] = arr
                vars_used.add(k)
            else:
                print(c("Ignoring array declaration %s as it produces empty sequence" % v).magenta)

var_sets_difference = expected_vars-vars_used
if any(var_sets_difference):
    print(c("Not all variables defined, missing: %s" % ", ".join(var_sets_difference)).red)
    exit(1)

dst_output['name'] = template_data['name']
dst_output['sequence'] = {}
dst_output['jobs'] = {}

import itertools
options = {"number": [1,2,3], "color": ["orange","blue"] }
product = [x for x in apply(itertools.product, arrays.values())]
kv = [dict(zip(arrays.keys(), p)) for p in product]

for k in kv:
    for j,v in jobs.iteritems():
        template = Template(j, undefined=DebugUndefined)
        name = template.render(**k)
        template = Template(v['command'], undefined=DebugUndefined)
        command = template.render(**k)
        dst_output['jobs'][name] = v
        dst_output['jobs'][name]['command'] = command
    for s,v in sequence.iteritems():
        template = Template(s, undefined=DebugUndefined)
        name = template.render(**k)
        template = Template(v, undefined=DebugUndefined)
        nextjob = template.render(**k)
        dst_output['sequence'][name] = nextjob

#import pprint
#pprint.pprint(dst_output)

print yaml.dump(dst_output)

sys.exit(0)






# print("All variables have been defined, generating jobs")

#template_data['command'] = '            ' + template_data['command'].replace("\n", "\n            ")
#template_data['jobs'] = '            ' + template_data['jobs'].replace("\n", "\n            ")

# start rendering loop 
template = Template(template_data['jobs'], undefined=DebugUndefined)
after_literals_rendered = template.render(**literals)

jobs = []

#if walltime<>'':
#    walltime = 'walltime: "%s"' % walltime

#if queuename<>'':
#    queuename = 'queuename: "%s"' % queuename

#if name=='':
#    name = 'job_{{loop.index}}'

#after_literals_rendered = "   job{{loop.index}}: \n        nodes: 0\n        walltime: \"00:30:00\"\n        command: |+\n%s\n" % after_literals_rendered
#after_literals_rendered = "   job__{{loop.index}}: \n        nodes: 1\n        %s\n        %s\n        command: |+\n%s\n" % (walltime, queuename, after_literals_rendered)
after_literals_rendered = "   job__%s: \n        nodes: 1\n        %s\n        %s\n        command: |+\n%s\n" % (name, walltime, queuename, after_literals_rendered)

for k,v in arrays.iteritems():
    #after_literals_rendered = "{%% for %s in %s %%}\n   job{{loop.index}}: |+\n%s\n{%% endfor %%}" % (k, v, after_literals_rendered)
    after_literals_rendered = "{%% for %s in %s %%}\n%s\n{%% endfor %%}" % (k, v, after_literals_rendered)

template = Template(after_literals_rendered, undefined=StrictUndefined)
print("name: %s\njobs:\n" % ''.join(random.choice(string.lowercase) for x in range(20)))
print(template.render())
print('sequence: ')


# finally: write data into output
