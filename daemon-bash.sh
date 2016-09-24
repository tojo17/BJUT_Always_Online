#!/bin/bash
cd $(dirname ${0})
nohup python3 ./online.py > ./log.txt 2>&1 &