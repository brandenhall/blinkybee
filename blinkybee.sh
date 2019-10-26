#!/bin/bash

BASEDIR=$(dirname "$0")

cd $BASEDIR
source ./venv/bin/activate && python -m blinkybee.blinkybee
