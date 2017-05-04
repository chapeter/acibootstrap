#!/bin/bash

ansible-playbook -i acibootstrap/files/vars/hosts -M ansible/library/ acibootstrap.yaml -v
