sudo wget http://s3tools.org/repo/RHEL_6/s3tools.repo -O /etc/yum.repos.d/s3tool.repo
sudo yum --disablerepo=* --enablerepo=s3tools install -y s3cmd
echo """
access_key = $CFN_ACCESS_KEY
secret_key = $CFN_SECRET_KEY
""" > ~/.s3cfg
