
sudo yum -y install gcc-c++

wget http://www.cmake.org/files/v2.8/cmake-2.8.10.2.tar.gz
tar xzf cmake-2.8.10.2.tar.gz 

cd cmake-2.8.10.2
./configure
gmake
sudo gmake install 

wget 'http://downloads.sourceforge.net/project/freeimage/Source%20Distribution/3.15.4/FreeImage3154.zip?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Ffreeimage%2F' -O FreeImage.zip
unzip FreeImage.zip
cd FreeImage
make
sudo make install

cd /home/ec2-user/dpxdt-1/pdiff
cmake .
make
sudo make install

