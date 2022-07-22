#!/usr/bin/env bash

# The user for which some utilities will be installed
user=${1:-vagrant}

# https://www.digitalocean.com/community/tutorials/package-management-basics-apt-yum-dnf-pkg
yum check-update
yum install -y yum-utils gnupg2.x86_64 \
    ca-certificates git curl wget unzip \
    pycairo-devel dejavu-fonts-common freetype-devel java-1.8.0-openjdk-devel \
    xorg-x11-server-Xvfb libvirt-gconfig device-mapper-persistent-data lvm2-devel \
    lvm2-python-libs \
    gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel


# Install NodeJS/npm
# https://computingforgeeks.com/how-to-install-latest-nodejs-on-centos-fedora/
curl -sL https://rpm.nodesource.com/setup_10.x | sudo bash -
yum  -y install gcc-c++ make nodejs 

# Install docker
# https://docs.docker.com/engine/install/centos/
#   remove any old docker packages
yum remove -y docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
#   add repo
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
#   perform install
yum check-update
yum install -y docker-ce docker-ce-cli containerd.io

# Allow the user to use docker
usermod -aG docker $user

# See https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html
echo vm.max_map_count=262144 > /etc/sysctl.d/vm_max_map_count.conf
sysctl --system

# Install docker-compose, cookiecutter and pipenv for the user
#su -c "pip3 install --user cookiecutter pipenv docker-compose" $user

# enable and start docker
systemctl enable docker
systemctl start docker


mkdir /home/vagrant/bin
cd /home/vagrant/bin
CHROMEDRIVER_VERSION=$(curl "http://chromedriver.storage.googleapis.com/LATEST_RELEASE")
wget "http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
rm chromedriver_linux64.zipi
chown vagrant:vagrant /home/vagrant/bin 
# install pipenv
#pip3 install pipenv

#build environment
#../build_env.sh
