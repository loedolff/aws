# Originally from https://www.djangoproject.com/download/

sudo yum -y install git

s3cmd get s3://hll-bootstrap/tars/Django-1.5.1.tar.gz  --force

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
