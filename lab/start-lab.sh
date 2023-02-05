#!/bin/bash

set -eo pipefail
set -x

sudo docker run -d --init --rm --name=wave-training -p 8080:8080 -p 10101:10101 -p 10102:10102 -p 10103:10103 wave-aquarium-lab
sudo docker exec -d -w /root/wave wave-training ./waved
