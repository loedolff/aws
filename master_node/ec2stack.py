import subprocess
import random
import string
import time
import re
import os
import traceback
import sys
import stat

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

def run_command(command):
  """run a shell command"""
  p = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True)
  output = [] 
  for line in iter(p.stdout.readline, b''):
    print line
    output.append(line)
  return "\n".join(output)


def get_identifiers(stack_description):
  """get maste node name"""
  global master_node
  global security_group
  m = re.match(r".*MasterNodePublicDNSName=(.*);PuppetClientSecurityGroup=(.*) .*", stack_description)
  if m is not None:
    master_node = m.group(1)
    security_group = m.group(2)
  else:
    raise Exception('Could not read Master Node or Security Group names', stack_description)



def get_output_dir():
  return 'stacks/' + STACK_NAME + '/'

def make_output_dir():
  if not os.path.exists(get_output_dir()):
    os.makedirs(get_output_dir())

def write_ssh_mn_script():
  """"write a convenience shell script to log into the master node"""
  f = open(get_output_dir() + 'ssh-mn.sh', 'w')
  f.write('ssh -t -o "StrictHostKeyChecking no" -i ~/.ssh/mykeypair.pem ' +
    'ec2-user@' + master_node + ' "$1"')
  os.chmod(f.name, stat.S_IRWXU)
  f.close()

def write_scp_mn_script():
  """"write a convenience shell script to copy a file to the master node"""
  f = open(get_output_dir() + 'scp-mn.sh', 'w')
  f.write('scp -i ~/.ssh/mykeypair.pem $1 ec2-user@' + master_node + ":temp/\n")
  os.chmod(f.name, stat.S_IRWXU)
  f.close()

def write_ss_mn_script():
  """write a convenience shell script to copy a local file to the remote and run it"""
  # make remote 'temp' dir
  run_ssh_command("mkdir temp"); 
  # write script to copy a local script to remote 'temp' and then execute it
  f = open(get_output_dir() + 'ss-mn.sh', 'w')
  f.write("DIR=`dirname $0`\n")
  f.write("$DIR/scp-mn.sh $1\n") 
  f.write("$DIR/ssh-mn.sh temp/`basename $1`\n")
  f.close()
  os.chmod(f.name, stat.S_IRWXU)
  

def run_ssh_command(command):
  """run an ssh command"""
  return run_command('ssh -t -o "StrictHostKeyChecking no" -i ~/.ssh/mykeypair.pem ' + 
      "ec2-user@" + master_node + ' "' + command + '"')

def wait_for_ssh():
  """wait for SSH port to become available"""
  output = run_ssh_command("echo")
  for i in range(20):
    if 'Connection refused' not in output:
      break
    time.sleep(10)

def set_cfn_credentials():
  """write the CFN credentials into .bashrc on remote host"""
  run_ssh_command("echo export CFN_ACCESS_KEY=" + os.environ.get('CFN_ACCESS_KEY') + " >> .bashrc")
  run_ssh_command("echo export CFN_SECRET_KEY=" + os.environ.get('CFN_SECRET_KEY') + " >> .bashrc")

