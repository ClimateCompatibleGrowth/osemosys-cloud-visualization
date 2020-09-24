#!/bin/bash

set -xue

git pull
source venv_asdf/bin/activate
pip3 install -r requirements.txt
rm -rf cache
sudo systemctl restart osemosys-cloud-visualization.service
exit
