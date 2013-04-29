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

# TODO: Make cloud formation logical-id a parameter

#
# INSTANCE	i-46a66d73	ami-ecbe2adc	ec2-54-245-133-5.us-west-2.compute.amazonaws.com	ip-10-254-25-107.us-west-2.compute.internal	running	mykeypair	0		t1.micro	2013-04-29T20:12:30+0000	us-west-2a	aki-fc37bacc	monitoring-enabled	54.245.133.5	10.254.25.107			ebs					paravirtual	xen	38a8acac-9ba0-4725-bcb8-b3fc7548b7c7_us-west-2a_1	sg-d35712e3	default	false	
#
# TAG	instance	i-46a66d73	aws:cloudformation:stack-name	hhh
#

def parse_output(output):
  """instance name"""
#  p = re.compile(r"INSTANCE(?:\t[\w-]+){3}\t([\w]+).*running.*")
#  p = re.compile(r"INSTANCE(?:\t[\w-]+){2}\t(.*)")
  p = re.compile(r"INSTANCE(?:\t[\w-]+){2}\t([-.\w]+).*running.*")
  found = False
  for m in p.finditer(output):
    found = True
    public_dns_name = m.group(1)
    print "------------------------------------"
    print "DNS = " + public_dns_name
    print "------------------------------------"
    m = p.search(output)
  if not found:
    print "!!!!! No instances found !!!!"
    

try:
  instances = run_command('ec2-describe-instances -H --filter "tag:aws:cloudformation:logical-id=WorkerGroup"')
  parse_output(instances)
 
#  make_output_dir()
#  write_ssh_mn_script()
#  write_scp_mn_script()
#  write_ss_mn_script()
#  wait_for_ssh();
#  set_cfn_credentials()
#  print "Master Node: ", master_node
#  print "Security Group: ", security_group

except Exception as instance:
  print traceback.format_exc()

