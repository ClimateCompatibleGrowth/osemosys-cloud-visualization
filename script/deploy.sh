#!/bin/bash

set -xue

git pull
source venv/bin/activate
pip3 install -r requirements.txt
rm -rf cache
sudo systemctl restart osemosys-cloud-visualization.service
exit
