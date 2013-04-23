import subprocess
import random
import string
import time
import re
import os
import traceback
import sys
import stat

STACK_NAME='bbb'
# STACK_NAME= ''.join(random.sample(string.lowercase, 3))

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

def create_stack():
  """execute a shell command to create a stack with a master node"""
  return run_command(
    ["cfn-create-stack " + STACK_NAME + " -f master-node.template"])

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

def wait_for_completion():
  """wait for stack creation to complete"""
  for i in range(100):
    output = run_command(["cfn-describe-stacks " + STACK_NAME])
    if "CREATE_COMPLETE" in output:
      break
    time.sleep(15)
  get_identifiers(output)


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
  f.write('scp -i ~/.ssh/mykeypair.pem $1 ec2-user@' + master_node + ":temp/\n")
  f.write('ssh -t -o "StrictHostKeyChecking no" -i ~/.ssh/mykeypair.pem ' +
    'ec2-user@' + master_node + ' temp/`basename $1`\n')
  os.chmod(f.name, stat.S_IRWXU)
  f.close()
  

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

# start creating client stack

# log into master node master and install PM 3
# get PM configuration from SCM
# run update on PM so it can configure itself (?)
# install mcollective

# wait for client to complete
# log into client and install puppet 3 client 
# point client to PM server
# classify client
# do puppet run on client

# more todo:
# would be nice to just write the instance name to a file rather than looking it up every time
# would be nice to create a script to easily ssh to new instance.  hey, that's related to previous statement :-)
 
try:
#  create_stack()
  wait_for_completion()
  make_output_dir()
  write_ssh_mn_script()
  write_scp_mn_script()
  write_ss_mn_script()
  wait_for_ssh();
  set_cfn_credentials()
  print "Master Node: ", master_node
  print "Security Group: ", security_group
except Exception as instance:
  print traceback.format_exc()

