import subprocess
import random
import string

STACK_NAME='stack1'
#STACK_NAME='stack'.join(random.sample(string.lowercase, 3))

def run_command(command):
  p = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    shell=True)
  for line in iter(p.stdout.readline, b''):
    print line

# create puppet master stack
def create_stack():
  return run_command(
    ["cfn-create-stack " + STACK_NAME + " -f puppet-master.template"])

# wait for completion
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
except Exception as inst:
  print "here"
  print inst
  print "and here"

