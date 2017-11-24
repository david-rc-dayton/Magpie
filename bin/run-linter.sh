#!/usr/bin/env bash

cd $(dirname ${0})/..

python -m pylint magpie.py
