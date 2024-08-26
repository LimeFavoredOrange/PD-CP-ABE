# Use the official Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set the maintainer label
LABEL maintainer="xinzhang.chen@yahoo.com"

# Install necessary packages
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y wget python3.7 python3.7-dev python3.7-distutils flex bison virtualenv git libgmp10 libgmp-dev openssl libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Create and activate a new virtual environment with Python 3.7
RUN virtualenv -p /usr/bin/python3.7 /opt/py37

# Clone the charm repository
RUN git clone https://github.com/JHUISI/charm /opt/charm

# Modify configure.sh and Makefile to remove sudo commands
RUN sed -i 's/sudo //g' /opt/charm/configure.sh && \
    sed -i 's/sudo //g' /opt/charm/deps/pbc/Makefile

# Install required Python packages
RUN /bin/bash -c "source /opt/py37/bin/activate && cd /opt/charm && pip install -r requirements.txt && pip install numpy"

# Run the configuration script and install the PBC library with debugging output
RUN /bin/bash -c "source /opt/py37/bin/activate && cd /opt/charm && ./configure.sh && echo 'Configure completed' && cd ./deps/pbc && make && echo 'Make completed' && ldconfig && cd -"

# Compile and install the charm library with debugging output
RUN /bin/bash -c "source /opt/py37/bin/activate && cd /opt/charm && make && echo 'Make completed' && make install && echo 'Make install completed' && ldconfig"

# Add a script to source the virtual environment
RUN echo 'source /opt/py37/bin/activate' >> ~/.bashrc

# Set the working directory to the home directory
WORKDIR /root

# Set the default command to run the bash shell
CMD ["/bin/bash"]
