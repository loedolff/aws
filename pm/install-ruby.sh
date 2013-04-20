
??? sudo yum -y install gem ruby-devel gcc rubygem-nokogiri
??? sudo yum install -y ruby ruby-libs ruby-mode ruby-rdoc ruby-irb ruby-ri ruby-docs 
??? sudo yum install -y ruby19 ruby19-devel rubygem-aws-sdk rubygem-json 

sudo yum install -y ruby19 ruby19-devel rubygem-aws-sdk rubygem-json 
sudo yum install -y gcc libxml2

???sudo yum install -y libxml2-devel libxslt libxslt-devel

# could probably just use local directory.  then also no need to "sudo" install gems...
???export GEM_HOME=/usr/lib/ruby/gems/1.8

sudo gem1.9 install nokogiri
sudo gem1.9 install aws-sdk

# and run it using, for example, ruby1.9 get.rb tars/Django-1.5.1.tar.gz

