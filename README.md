# ACIBOOTSTRAP

## Overview
ACIBOOTSTRAP is an application designed to help speed up ACI deployments by automating the common configuration elements of setting up ACI and building out a standardized port map for the fabric

## Prerequisites
Before running ACIBOOTSTRAP, the user must ensure that the APIC controllers have been setup through their initial setup wizard.



## Demo acibootstrap
acibootstrap requires a clean config of ACI.  To demo it is best to use against the ACI simulator.  This means it can all be done locally.  If you plan to do this many times; snapshot your fabric after a clean install.

### Demo Using the Simulator
1. Install Simulator OVA
2. Go through APIC setup wizard
3. Fill out the [ACI-Bootstrap-Tool](acibootstrap/files/vars/ACI-Bootstrap-Tool.xlsx), or fill out the Smartsheet webform if you have access
4. Start acibootstrap via:
  ```docker run -d -p 5000:5000 -p 5001:5001 -p 8001:8001 imapex/acibootstrap```
5. Open acibootstrap web page: ```http://0.0.0.0/5000```
6. Upload ACI-Bootstrap-Tool Excel sheet via webpage
7. Ensure APIC IP and user are correct, then press ```Run```
8. Watch the magic


### Demo Using a Real ACI Fabric
1. Cable and connect switches and APICs to each other
2. Connect Switches and APICs to OOB network
3. Connect physical equipment as listed in the Port-Map
2. Go through APIC setup wizard
3. Fill out the [ACI-Bootstrap-Tool](acibootstrap/files/vars/ACI-Bootstrap-Tool.xlsx) Excel Sheet, or fill out the Smartsheet webform if you have access
5. Do Fabric Discovery and use naming scheme of 1XX for leaf and 2XX for spine devices, starting with 101/201
4. Start acibootstrap via:
  ```docker run -d -p 5000:5000 -p 5001:5001 -p 8001:8001 imapex/acibootstrap```
5. Open acibootstrap web page: ```http://0.0.0.0/5000```
6. Upload ACI-Bootstrap-Tool Excel sheet via webpage
7. Ensure APIC IP and user are correct, then press ```Run```
8. Watch as acibootstrap configures your fabric

#### Port map
| port | device | info | related info |
|:---:|---|---| --- |
| 1 | l2-out| |
| 2 | L3-out| Speed Defined in XLSX |
| 3 | L2 extention vpc | 10g Used for ACI migrate
| 4 | L2 extention vpc | 10g Used for ACI migrate
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
| 46 | apic3 | 10g |
| 47 | apic2 | 10g |
| 48 | apic1 | 10g |


## Manual Work that needs to be done AFTER acibootstrap
Once acibootstrap is complete, you will be left with all the OOB mgmt taken care of, physical connections to devices listed in the port-map done, vmm integration, a sample tenant, and EPG's advertised into vCenter.

Likley you will want to setup more tenants to show off ACI.  You may also want to setup some new EPG's or Tenants




# Nerdy Stuff
## Architecture
acibootstrap is primarily an Ansible playbook used to configure Cisco ACI fabric.

For easy deployment and viewing I include a web wrapper around this playbook.  At the heart of acibootstrap we have 3 main webservers:
1. Flask to host the main application and the main webpage you see
2. Flask application that hosts the "Run" Button
3. Tornado server running tailon to monitor logs

I had to host the "RUN" button in a seperate webserver so that the main page would not refresh and clear the tailon screen.  Likely doing some threading work in Python could have fixed this as well.



## Ansible
Most of the ansible work I have was based off of Jason Edelman's aci-rest module from his repo [aci-ansible](https://github.com/jedelman8/aci-ansible).  Much of my learning came from Joel King's [ansible-aci](https://github.com/joelwking/ansible-aci) repo.  I stuck mainly to Jason's aci-rest as it was handeling JSON.  But I looked at the custom modules from Joel to create a few that I wrote that you'll find in: ```acibootstrap/ansible/libary```.  Data parsing in Ansible was a mystery to me...handling nested Dictionarys with lists seemed impossible so I re-built how data was sent to Ansible with a few of these modules.

In general the process through the playbook is pretty simple.  Build json from jinja2 template using variables defined from Excel file.  Then push json to APIC.

To add tasks simply configure your object in ACI, download json and templitize.  Templates reside in ```acibootstrap/files/configs/templates```.  Follow the same tasks to turn the jinja template into json and push to ACI.
