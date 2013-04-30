import subprocess
import random
import string
import time
import re
import os
import traceback
import sys
import stat
from cmd_utils import *

class EC2Stack:

  def __init__(self, stack_name, template_file):
    self.stack_name = stack_name
    self.template_file  = template_file

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

