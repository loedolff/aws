import subprocess
import random
import string
import time
import re
import os
import traceback
import sys
import stat
from ec2stack import EC2Stack

try:
  ec2Stack = EC2Stack('hhh', "worker-stack.template")  
  ec2Stack.create_stack()
  ec2Stack.wait_for_completion()

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

