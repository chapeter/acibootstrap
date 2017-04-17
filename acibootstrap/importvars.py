#!/usr/bin/env python
__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

import openpyxl
import yaml

workbook = openpyxl.load_workbook("acibootstrap/files/vars/acibootstrap.xlsx", data_only=True)

print(workbook.sheetnames)

fabric_pol = workbook["fabric_pol"]
vcenter = workbook["vcenter"]
poc_tenant = workbook["poc_tenant"]
mgmt = workbook["mgmt"]


def getFabricPolicyVariables():
    fabric_pol_vars = {}
    for row in fabric_pol.rows:
        fabric_pol_vars[row[0].value] = row[1].value
    return fabric_pol_vars

def getVMMVars():
    vmm_vars = {}
    vmm_vars['vmmpool'] = 'vmmpool'
    vmm_vars['vmmpool_start'] = vcenter['A3'].value
    vmm_vars['vmmpool_end'] = vcenter['B3'].value
    vmm_vars['vcenter_ip'] = vcenter['B6'].value
    vmm_vars['vcenter_dc'] = vcenter['B7'].value
    vmm_vars['vcenter_user'] = vcenter['B8'].value
    vmm_vars['vcenter_pass'] = vcenter['B9'].value

    return vmm_vars

def getMGMTVars():
    mgmt_vars = {}
    mgmt_vars['oob_from'] = mgmt['B3'].value
    mgmt_vars['oob_to'] = mgmt['C3'].value
    mgmt_vars['oob_gw'] = mgmt['D3'].value




    return mgmt_vars

def getPocTenantVariables():
    tenant_name = poc_tenant['B2'].value
    poc_tenant_vars = {
        'tenant': {
            'name':tenant_name,
            'external_subnets':[],
            'private_subnets':[]}}


    counter = 0
    for row in poc_tenant.rows:
        if row[0].value == tenant_name:
            subnet = {'name': counter, 'address': row[2].value}
            if row[1].value == "external":
                poc_tenant_vars['tenant']['external_subnets'].append(subnet)
            else:
                poc_tenant_vars['tenant']['private_subnets'].append(subnet)
        counter += 1
    return poc_tenant_vars

def saveYAML(var):
    with open('acibootstrap/files/vars/acibootstrap_vars.yml', 'w') as outfile:
        yaml.safe_dump(var, outfile, default_flow_style=False)

def mergeDicts(x, y):
    z = x.copy()
    z.update(y)
    return z

fabric_pol_vars = getFabricPolicyVariables()
poc_tenant_vars = getPocTenantVariables()
vmm_vars = getVMMVars()
mgmt_vars = getMGMTVars()

a = mergeDicts(fabric_pol_vars, poc_tenant_vars)
b = mergeDicts(a, vmm_vars)
c = mergeDicts(b, mgmt_vars)


saveYAML(c)
