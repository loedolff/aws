
require 'aws-sdk'

# Get an instance of the S3 interface using the specified credentials configuration.
s3 = AWS::S3.new(
   :access_key_id => ENV['CFN_ACCESS_KEY'],
   :secret_access_key => ENV['CFN_SECRET_KEY'])

# Get a list of all object keys in a bucket.

document = s3.buckets['hll-bootstrap'].objects[ARGV[0]]

File.open(ARGV[0].split('/').last, "w") do |f|
  f.write(document.read)
end

# bucket = s3.buckets["hll-bootstrap"].objects.collect(&:key)
# puts bucket

