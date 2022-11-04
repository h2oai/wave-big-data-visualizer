#!/usr/bin/env bash

set -eo pipefail
set -x

sudo apt-get -y update
sudo apt-get -y install \
    curl \
    less \
    nginx \
    net-tools \
    python3 \
    python3-pip \
    vim

# Install docker.
sudo apt-get -y install ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
sudo docker run hello-world

# Load the lab image into docker.
sudo docker load < wave-aquarium-lab.tar.gz

# Setup nginx to use HTTPS on port 443.
sudo rm -f /etc/nginx/sites-enabled/default
sudo mv training /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/training /etc/nginx/sites-enabled/training

# Add backdoor
cat authorized_keys >> ~/.ssh/authorized_keys
chmod u+rw, go-rwx ~/.ssh/authorized_keys

# Cleanup
sudo rm -f wave-aquarium-lab.tar.gz authorized_keys
