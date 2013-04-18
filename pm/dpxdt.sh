yum install -y git
mkdir temp
cd temp

# No need for this
# wget http://peak.telecommunity.com/dist/ez_setup.py
# sudo python ez_setup.py

# need to store this in my own S3 location...
wget https://www.djangoproject.com/download/1.5.1/tarball/ -o Django-1.5.1.tar.gz
tar xzvf Django-1.5.1.tar.gz
cd Django-1.5.1
sudo python setup.py install

