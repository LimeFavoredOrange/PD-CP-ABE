#!/bin/bash

# OS: Ubuntu 22.04

# Add the deadsnakes PPA to the sources list
sudo add-apt-repository -y ppa:deadsnakes/ppa

# Update the package list
sudo apt update

sudo apt install -y python3.7 python3.7-dev python3.7-distutils flex bison virtualenv git libgmp10 libgmp-dev openssl libssl-dev

# Create a new virtual environment with Python 3.7
virtualenv -p /usr/bin/python3.7 py37

# Activate the virtual environment
source py37/bin/activate

# Clone the charm repository
git clone https://github.com/JHUISI/charm

# Install the required python packages
cd charm
pip install -r requirements.txt
pip install -y numpy

# Run the configuration script
./configure.sh

# Compile and install the PBC library
cd ./deps/pbc && make && sudo ldconfig && cd -

# Compile and install the charm library
make
make install && sudo ldconfig
