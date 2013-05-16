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

class EC2Instance:

  def __init__(self, stack, public_dns_name, instance_id):
    self.stack = stack
    self.public_dns_name = public_dns_name
    self.instance_id = instance_id

  def get_output_dir(self):
    return self.stack.get_output_dir()

  def get_ssh_script(self):
    return 'ssh-' + self.instance_id  + '.sh'

  def get_scp_to_script(self):
    return 'scp-to-' + self.instance_id + '.sh'

  def get_scp_from_script(self):
    return 'scp-from-' + self.instance_id + '.sh'

  def write_ssh_script(self):
    """"write a convenience shell script to log into the instance"""
    f = open(self.get_output_dir() + self.get_ssh_script(), 'w')
    f.write('ssh -t -o "StrictHostKeyChecking no" -i ~/.ssh/mykeypair.pem ' +
      'ec2-user@' + self.public_dns_name + ' "$1"')
    os.chmod(f.name, stat.S_IRWXU)
    f.close()

  def run_ssh_command(self, command):
    run_command(self.get_output_dir() + self.get_ssh_script() + ' "' + command + '"');

  def write_scp_to_script(self):
    """"write a convenience shell script to copy a file to the master instance"""
    f = open(self.get_output_dir() + self.get_scp_to_script(), 'w')
    f.write('scp -i ~/.ssh/mykeypair.pem $1 ec2-user@' + self.public_dns_name + ":temp/\n")
    os.chmod(f.name, stat.S_IRWXU)
    f.close()

  def write_scp_from_script(self):
    """"write a convenience shell script to copy a file from the master instance"""
    f = open(self.get_output_dir() + self.get_scp_from_script(), 'w')
    f.write('scp -i ~/.ssh/mykeypair.pem ec2-user@' + self.public_dns_name + ":$1 ~/temp/\n")
    os.chmod(f.name, stat.S_IRWXU)
    f.close()

  def write_ss_script(self):
    """write a convenience shell script to copy a local file to the remote and run it"""
    # make remote 'temp' dir
    self.run_ssh_command("mkdir -p temp")
    # write script to copy a local script to remote 'temp' and then execute it
    f = open(self.get_output_dir() + 'ss-' + self.instance_id + '.sh', 'w')
    f.write("DIR=`dirname $0`\n")
    f.write("$DIR/" + self.get_scp_to_script() + " $1\n")
    f.write("$DIR/" + self.get_ssh_script() + " temp/`basename $1`\n")
    f.close()
    os.chmod(f.name, stat.S_IRWXU)

  def write_all_scripts(self):
    self.stack.make_output_dir()
    self.write_ssh_script()
    self.write_scp_to_script()
    self.write_scp_from_script()
    self.write_ss_script()

  def write_cfn_keys(self):
    self.run_ssh_command(
      "sed -i '/CFN_.*_KEY/d' .bashrc && "
      "echo export CFN_ACCESS_KEY=" + os.environ.get('CFN_ACCESS_KEY') + " >> .bashrc && "
      "echo export CFN_SECRET_KEY=" + os.environ.get('CFN_SECRET_KEY') + " >> .bashrc")

