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
  """execute a shell command to create a puppet master stack"""
  return run_command(
    ["cfn-create-stack " + STACK_NAME + " -f puppet-master.template"])

def get_identifiers(stack_description):
  """get puppet_master name"""
  global puppet_master
  global security_group
  m = re.match(r".*PuppetMasterPublicDNSName=(.*);PuppetClientSecurityGroup=(.*) .*", stack_description)
  if m is not None:
    puppet_master = m.group(1)
    security_group = m.group(2)
  else:
    raise Exception('Could not read Puppet Master or Security Group names', stack_description)

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

def write_go_pm_script():
  """"write a convenience shell script to log into puppet master"""
  f = open(get_output_dir() + 'go-pm.sh', 'w')
  f.write('ssh -t -o "StrictHostKeyChecking no" -i ~/.ssh/mykeypair.pem ' +
    'ec2-user@' + puppet_master + ' "$1"')
  os.chmod(f.name, stat.S_IRWXU)
  f.close()

def run_ssh_command(command):
  """run an ssh command"""
  return run_command('ssh -t -o "StrictHostKeyChecking no" -i ~/.ssh/mykeypair.pem ' + 
      "ec2-user@" + puppet_master + ' "' + command + '"')

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

# log into puppet master and install PM 3
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
  make_output_dir();
  write_go_pm_script()
  wait_for_ssh();
  set_cfn_credentials();
  print "Puppet Master: ", puppet_master
  print "Security Group: ", security_group
except Exception as instance:
  print traceback.format_exc()

