import subprocess
import random
import string
import time
import re

# STACK_NAME='yjd'
STACK_NAME= ''.join(random.sample(string.lowercase, 3))

# run a shell command
def run_command(command):
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

# create puppet master stack
def create_stack():
  return run_command(
    ["cfn-create-stack " + STACK_NAME + " -f puppet-master.template"])

# get puppet_master name
def get_identifiers(stack_description):
  global puppet_master
  global security_group
  m = re.match(r".*PuppetMasterPublicDNSName=(.*);PuppetClientSecurityGroup=(.*) .*", stack_description)
  if m is not None:
    puppet_master = m.group(1)
    security_group = m.group(2)
  else:
    raise Exception('Could not read Puppet Master or Security Group names', stack_description)

# wait for completion
def wait_for_completion():
  for i in range(10):
    output = run_command(["cfn-describe-stacks " + STACK_NAME])
    if "CREATE_COMPLETE" in output:
      break
    time.sleep(10)
  get_identifiers(output)

# test ssh

def test_ssh():
  for i in range(10):
    output = run_command('ssh -t -o "StrictHostKeyChecking no" -i ~/.ssh/mykeypair.pem ' + 
      "ec2-user@" + puppet_master + " ls -al")
    if 'Connection refused' not in output:
      break
    time.sleep(5)
  print '-----------------------'

# get security group from description
# start creating client stack

# log into puppet master and install PM 3
# get PM configuration from SCM
# run update on PM so it can configure itself (?)

# wait for client to complete
# log into client and install puppet 3 client 
# point client to PM server
# classify client
# do puppet run on client
 
try:
  create_stack()
  wait_for_completion()
  print "Puppet Master: ", puppet_master
  print "Security Group: ", security_group
  test_ssh();
except Exception as instance:
  print instance

