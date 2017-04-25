#!/bin/bash

python acibootstrap/importvars.py
ansible-playbook -i acibootstrap/files/vars/hosts -M ansible/library/ tests.yaml -v
