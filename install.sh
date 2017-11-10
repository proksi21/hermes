#!/bin/bash

cd /root/hermes
apt update && apt full-upgrade
apt install python3 python3-pip
pip3 install twisted
git clone https://github.com/ericsomdahl/python-bittrex.git
cd python-bittrex
python3 setup.py install
cd /root/hermes
