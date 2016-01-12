#!/bin/sh

# Generates a "coverage.xml" file
python-coverage run setup.py check
python-coverage xml
