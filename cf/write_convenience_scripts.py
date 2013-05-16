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
from ec2stack import EC2Stack

# TODO: Make cloud formation stack name (the logical-id) a parameter

def get_instances(stack):
  """instance name"""
  command = ('ec2-describe-instances -H --filter "tag:aws:cloudformation:logical-id=WorkerGroup" ' 
    '--filter "tag:aws:cloudformation:stack-name=' + stack.stack_name + '"')
  output = run_command(command)
  dns_pattern = re.compile(r"INSTANCE\t([\w-]+)\t[-.\w]+\t([-.\w]+).*(?:running|pending).*")
  found = False
  for m in dns_pattern.finditer(output):
    found = True
    instance_id = m.group(1)
    public_dns_name = m.group(2)
    yield EC2Instance(stack, public_dns_name, instance_id)
    m = dns_pattern.search(output)
  if not found:
    print "!!!!! No instances found !!!!!"

def write_instance_scripts(stack):
  dns_names = get_instances(stack)
  for instance in dns_names:
    instance.write_all_scripts()  
    instance.write_cfn_keys()

try:
  for stack in EC2Stack.get_stacks():
    print ">>>> Processing stack: " + stack.stack_name
    stack.clean_output_dir()
    write_instance_scripts(stack)
    stack.write_set_capacity_script()
 
except Exception as instance:
  print traceback.format_exc()

