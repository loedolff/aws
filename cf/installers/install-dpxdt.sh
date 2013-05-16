# Originally from https://www.djangoproject.com/download/
# s3cmd get s3://hll-bootstrap/tars/Django-1.5.1.tar.gz  --force

# Originally from wget https://phantomjs.googlecode.com/files/phantomjs-1.9.0-linux-x86_64.tar.bz2
s3cmd get s3://hll-bootstrap/tars/phantomjs-1.9.0-linux-x86_64.tar.bz2 --force
bzip2 -d phantomjs-1.9.0-linux-x86_64.tar.bz2 
mkdir -p ~/tools
tar xf phantomjs-1.9.0-linux-x86_64.tar -C ~/tools/

# Uploaded these by running package.sh and upload.shscripts in dpxdt distribution
s3cmd get s3://hll-bootstrap/tars/dpxdt-1.zip --force
s3cmd get s3://hll-bootstrap/tars/flask.zip --force
s3cmd get s3://hll-bootstrap/tars/flask-wtf.zip --force
s3cmd get s3://hll-bootstrap/tars/jinja2.zip --force
s3cmd get s3://hll-bootstrap/tars/itsdangerous.zip --force
s3cmd get s3://hll-bootstrap/tars/werkzeug.zip --force

unzip flask.zip
unzip flask-wtf.zip
unzip jinja2.zip
unzip itsdangerous.zip
unzip werkzeug.zip
unzip dpxdt-1.zip
