#!/bin/bash


tailon -f acibootstrap/logs/ansible.log -F -b 0.0.0.0:8001 &
python run.py &

python upload.py