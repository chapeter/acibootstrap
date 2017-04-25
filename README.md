# ACIBOOTSTRAP

## Overview
ACIBOOTSTRAP is an application designed to help speed up ACI deployments by automating the common configuration elements of setting up ACI and building out a standardized port map for the fabric

## Prerequisites
Before running ACIBOOTSTRAP, the user must ensure that the APIC controllers have been setup through their initial setup wizard.  

Users need to fill the acibootstrap Excel sheet here: [acibootstrap/files/vars/acibootstrap.xlsx](acibootstrap/files/vars/acibootstrap.xlsx)



## Using acibootstrap
1. Cable and connect switches and APICs to each other
2. Connect Switches and APICs to OOB network
3. Fill out the acibootstrap Excel workbook: [acibootstrap.xlsx](acibootstrap/files/vars/acibootstrap.xlsx)
4. Run acibootstrap
5. Upload Excel workbook to acibootstrap
6. Run


## Port map
| port | device | info | related info |
|:---:|---|---| --- |
| 1 | l2-out| |
| 2 | L3-out| Speed Defined in XLSX|
| 20 | UCS-FI A| vpc-1 |
| 21 | UCS-FI A| vpc-1 |
| 22 | UCS-FI B| vpc-2 |
| 23 | UCS-FI B| vpc-2|
| 30 | Rack Servers | 10g vpc |
| 31 | Rack Servers | 10g vpc |
| 32 | Rack Servers | 10g vpc |
| 33 | Rack Servers | 10g vpc |
| 34 | Rack Servers | 1g vpc |
| 35 | Rack Servers | 1g vpc |
| 36 | Rack Servers | 1g vpc |
| 37 | Rack Servers | 1g vpc |
| 38 | Rack Servers | 1g vpc |
| 39 | Rack Servers | 10g |
| 40 | Rack Servers | 10g |
| 41 | Rack Servers | 10g |
| 42 | Rack Servers | 1g |
| 43 | Rack Servers | 1g |
| 44 | Rack Servers | 1g |
| 45 | Rack Servers | 1g |
| 46 | apic3 | 1g |
| 47 | apic2 | 1g |
| 48 | apic1 | 1g |




## To Do
* [ ] Fabric Discovery
* [ ] Download file section
* [ ] Routed out selection for demo tenant
* [ ] Delivery packaging
* [ ] VMM attachment to EPG



## Manual Work that needs to be done AFTER acibootstrap



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
