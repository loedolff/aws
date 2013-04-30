import subprocess
import random
import string
import time
import re
import os
import traceback
import sys
import stat
from cmd_utils import run_command

# TODO: Make cloud formation stack name (the logical-id) a parameter

def write_convenience_scripts(stack_name, dns_names):
  print stack_name + " | " + dns_names

def parse_output(output):
  """instance name"""
  dns_pattern = re.compile(r"INSTANCE(?:\t[\w-]+){2}\t([-.\w]+).*(?:running|pending).*")
  found = False
  for m in dns_pattern.finditer(output):
    found = True
    public_dns_name = m.group(1)
    print "DNS = " + public_dns_name
    yield public_dns_name
    m = dns_pattern.search(output)
  if not found:
    print "!!!!! No instances found !!!!!"
    
def process_stack(stack_name):
  command = ('ec2-describe-instances -H --filter "tag:aws:cloudformation:logical-id=WorkerGroup" ' 
    '--filter "tag:aws:cloudformation:stack-name=' + stack_name + '"')
  dns_names = parse_output(run_command(command))
  for n in dns_names:
    write_convenience_scripts(stack_name, n)

try:
  output = run_command('cfn-describe-stacks')
  p = re.compile(r"STACK\s+([\w-]+)\s+CREATE_COMPLETE")
  found = False
  for m in p.finditer(output):
    found = True
    stack_name = m.group(1)
    print ">>>> Processing stack: " + stack_name
    process_stack(stack_name)
  if not found:
    print "!!!!! No stacks found !!!!!"
 
except Exception as instance:
  print traceback.format_exc()

