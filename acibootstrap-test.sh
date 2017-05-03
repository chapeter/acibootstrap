#!/bin/bash

python acibootstrap/importvars.py
ansible-playbook -i acibootstrap/files/vars/hosts -M ansible/library/ acibootstrap-test.yaml -v
