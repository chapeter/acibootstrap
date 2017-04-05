#!/bin/bash

python acibootstrap/importvars.py
ansible-playbook -i acibootstrap/files/hosts -M ansible/library/ acibootstrap.yaml -v