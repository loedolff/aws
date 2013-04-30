
sudo yum install -y ruby19 ruby19-devel 
sudo yum install -y gcc libxml2 libxml2-devel libxslt libxslt-devel

# gems are not installed using 'sude'.  they are installed in the user's home directory

gem1.9 install --no-rdoc --no-ri nokogiri aws-sdk json

