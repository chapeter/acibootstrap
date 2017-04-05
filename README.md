# ACIBOOTSTRAP

## Overview
ACIBOOTSTRAP is an application designed to help speed up ACI deployments by automating the common configuration elements of setting up ACI.

## Prerequisites
Before running ACIBOOTSTRAP, the user must ensure that the APIC controllers have been setup through their initial setup wizard.  After than ACIBOOTSTRAP can be used.


## Directory Structure
```
.
├── ansible
│   ├── aci-ansible
│   ├── ansible-aci
│   ├── library
│   └── vars
├── files
│   ├── cobra
│   ├── configs
│   ├── hosts
│   └── wiper.ini
├── images
├── Dockerfile
├── README.md
├── acibootstrap-cleanup.yaml
├── acibootstrap.retry
├── acibootstrap.xlsx
├── acibootstrap.yaml
├── scratchpad.md
├── scratchpad.pdf
├── tests.retry
└── tests.yaml
```

### Important files
* ```ansible/```: files needed to be referenced for ansible
  * ```library/``` which contains the used modules needed for acibootstrap playbooks  
  * ```vars/``` contains the variables used in the acibootstrap playbooks.  All other directories are for development purposes only

* ```files/```
  * ```cobra/```: currently not used, but contains the associated cobra files for the ACI images we may put in ```files/images/```
  * ```configs/```: this is one of the most critial components of acibootstrap.  This contains the template type configs we will be pushing via ansible.
    * ```templates/```: these are the base templates that we use to create the files we push to the ACI fabric
    * ```dynamic/```: files built from template files go here.  They will be converted into .json with real values and placed here
    * ```custom/```: depricated.
    * ```static/```: files not needed to be templitized and dynamically created

## To Do
* [ ] Fabric Discovery
* [ ] Set OOB for switches
* [ ] Setup VMM integration for VMware
* [ ] Create XLSX to YAML variable import for user defined criteria
* [x] Streatch [Flask web upload](http://flask.pocoo.org/docs/0.12/patterns/fileuploads/)
* [ ] Tail logs for online viewing of scripts

## Manual Work that needs to be done AFTER acibootstrap
