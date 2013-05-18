# execute as sudo

# pdiff-dist contains files generate as part of the output of running build-pdiff
# currently this zip file is hand crafted, but i should really create it at the end of build-pdiff!

s3cmd get s3://hll-bootstrap/tars/pdiff-dist.zip --force

unzip pdiff-dist.zip
cd pdiff-dist

sudo install -d //usr/include //usr/lib

# try without these next time (i think it's only needed for compiling or static linking, which we don't care about)
# install -m 644 -o root -g root FreeImage.h //usr/include
# install -m 644 -o root -g root libfreeimage.a //usr/lib

sudo install -m 755 -o root -g root libfreeimage-3.15.4.so //usr/lib
sudo ln -sf libfreeimage-3.15.4.so //usr/lib/libfreeimage.so.3
sudo ln -sf libfreeimage.so.3 //usr/lib/libfreeimage.so

sudo ldconfig

sudo cp perceptualdiff /usr/local/bin/

