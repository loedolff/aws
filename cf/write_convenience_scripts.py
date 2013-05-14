import subprocess
import random
import string
import time
import re
import os
import traceback
import sys
import stat
import shutil
from cmd_utils import run_command
from ec2instance import EC2Instance

# TODO: Make cloud formation stack name (the logical-id) a parameter

def get_instances(stack_name):
  """instance name"""
  command = ('ec2-describe-instances -H --filter "tag:aws:cloudformation:logical-id=WorkerGroup" ' 
    '--filter "tag:aws:cloudformation:stack-name=' + stack_name + '"')
  output = run_command(command)
  dns_pattern = re.compile(r"INSTANCE\t([\w-]+)\t[-.\w]+\t([-.\w]+).*(?:running|pending).*")
  found = False
  for m in dns_pattern.finditer(output):
    found = True
    instance_id = m.group(1)
    public_dns_name = m.group(2)
    yield EC2Instance(stack_name, public_dns_name, instance_id)
    m = dns_pattern.search(output)
  if not found:
    print "!!!!! No instances found !!!!!"

def write_set_capacity_script(stack_name, auto_scaling_group_name):
  f = open('stacks/' + stack_name + "/set-desired-capacity.sh", 'w')
  f.write('as-set-desired-capacity ' + auto_scaling_group_name + ' --desired-capacity $1')
  os.chmod(f.name, stat.S_IRWXU)
  f.close()
    
def write_instance_scripts(stack_name):
  # clean directory
  shutil.rmtree("stacks/" + stack_name, ignore_errors = True)
  dns_names = get_instances(stack_name)
  for instance in dns_names:
    instance.write_all_scripts()  
    instance.write_cfn_keys()

try:
  output = run_command('cfn-describe-stacks')
  p = re.compile(r"STACK\s+([\w-]+)\s+CREATE_COMPLETE.*AutoScalingGroupName=([\w-]+)\s")
  found = False
  for m in p.finditer(output):
    found = True
    stack_name = m.group(1)
    print ">>>> Processing stack: " + stack_name
    write_instance_scripts(stack_name)
    write_set_capacity_script(stack_name, m.group(2))
  if not found:
    print "!!!!! No stacks found !!!!!"
 
except Exception as instance:
  print traceback.format_exc()

