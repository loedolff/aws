cd ~/temp
s3cmd get s3://hll-bootstrap/rpms/hadoop-1.0.4-1.x86_64.rpm
sudo yum install -y localinstall hadoop-1.0.4-1.x86_64.rpm
