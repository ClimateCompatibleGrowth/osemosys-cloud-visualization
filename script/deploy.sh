#!/bin/bash

set -e

git pull
source venv/bin/activate
pip3 install -r requirements.txt
sudo systemctl restart osemosys-cloud-visualization.service
exit
