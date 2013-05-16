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
from cmd_utils import *

class EC2Stack:

  def __init__(self, stack_name, template_file = None, 
               auto_scaling_group_name = None):
    self.stack_name = stack_name
    self.template_file  = template_file
    self.auto_scaling_group_name = auto_scaling_group_name

  def create_stack(self):
    """execute a shell command to create a stack with a master node"""
    run_command(
      "cfn-create-stack " + self.stack_name + " -f " + self.template_file)

  def wait_for_completion(self):
    """wait for stack creation to complete"""
    for i in range(100):
      output = run_command("cfn-describe-stacks " + self.stack_name)
      if "CREATE_COMPLETE" in output:
        break
      if "ROLLBACK_COMPLETE" in output:
        run_command("cfn-describe-stack-events " + self.stack_name)
        raise Exception('Stack creation error')
      time.sleep(15)

  def get_output_dir(self):
    return 'stacks/' + self.stack_name + '/'

  def clean_output_dir(self):
    # clean directory
    shutil.rmtree(self.get_output_dir(), ignore_errors = True)

  def make_output_dir(self):
    if not os.path.exists(self.get_output_dir()):
      os.makedirs(self.get_output_dir())

  def write_set_capacity_script(self):
    self.make_output_dir()
    f = open(self.get_output_dir() + "/set-desired-capacity.sh", 'w')
    f.write('as-set-desired-capacity ' + self.auto_scaling_group_name + 
            ' --desired-capacity $1')
    os.chmod(f.name, stat.S_IRWXU)
    f.close()
    
  @staticmethod
  def get_stacks():
    """ return a list of all stacks """
    output = run_command('cfn-describe-stacks')
    p = re.compile(r"STACK\s+([\w-]+)\s+CREATE_COMPLETE.*AutoScalingGroupName=([\w-]+)\s")
    found = False
    for m in p.finditer(output):
      found = True
      stack_name = m.group(1)
      print ">>>> Found stack: " + stack_name
      yield EC2Stack(stack_name, auto_scaling_group_name = m.group(2))
    if not found:
      print "!!!!! No stacks found !!!!!"

