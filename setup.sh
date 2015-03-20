#!/bin/sh

# Setup a virtualenv
virtualenv env

# Install packages
env/bin/pip install -r requirements.txt
