#!/bin/sh
sudo apt-get update
sudo apt-get install curl
sudo apt-get install gcc
sudo apt-get install memcached
sudo apt-get install rsync
sudo apt-get install sqlite3
sudo apt-get install xfsprogs
sudo apt-get install git-core
sudo apt-get install libffi-dev
sudo apt-get install python-setuptools
sudo apt-get install python-coverage
sudo apt-get install python-dev
sudo apt-get install python-nose
sudo apt-get install python-xattr
sudo apt-get install python-eventlet
sudo apt-get install python-greenlet
sudo apt-get install python-pastedeploy
sudo apt-get install python-netifaces
sudo apt-get install python-pip
sudo apt-get install python-dnspython
sudo apt-get install python-mock

sudo pip install -r requirements.txt
sudo pip install -r test-requirements.txt
sudo pip install -U pip tox pbr virtualenv setuptools
sudo pip install PyECLib
sudo apt-get install libpython3.4-dev
sudo python setup.py develop
sudo apt-get remove python-six
sudo pip install -U six

