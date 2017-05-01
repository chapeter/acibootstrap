#!/usr/bin/env python
__author__ = 'Chad Peterson'
__email__ = 'chapeter@cisco.com'

import openpyxl
import yaml
import sys



def getFabricPolicyVariables(fabric_pol):
    fabric_pol_vars = {}
    for row in fabric_pol.rows:
        fabric_pol_vars[row[0].value] = row[1].value
    return fabric_pol_vars

def getVMMVars(vcenter):
    vmm_vars = {}
    vmm_vars['vmmpool'] = 'vmmpool'
    vmm_vars['vmmpool_start'] = vcenter['A3'].value
    vmm_vars['vmmpool_end'] = vcenter['B3'].value
    vmm_vars['vcenter_ip'] = vcenter['B6'].value
    vmm_vars['vcenter_dc'] = vcenter['B7'].value
    vmm_vars['vcenter_user'] = vcenter['B8'].value
    vmm_vars['vcenter_pass'] = vcenter['B9'].value

    return vmm_vars

def getMGMTVars(mgmt):
    mgmt_vars = {}
    mgmt_vars['oob_from'] = mgmt['B3'].value
    mgmt_vars['oob_to'] = mgmt['C3'].value
    mgmt_vars['oob_gw'] = mgmt['D3'].value




    return mgmt_vars

def getPocTenantVariables(poc_tenant):
    tenant_name = poc_tenant['B2'].value
    poc_tenant_vars = {
        'tenant': {
            'name':tenant_name,
            'external_subnets':[],
            'private_subnets':[],
            101:{},
            102:{},
            'ospf':{},
            'eigrp':{},
            'static':{}
            }}




    counter = 0
    for row in poc_tenant.rows:
        if row[0].value == tenant_name:
            subnet = {'name': counter, 'address': row[2].value}
            if row[1].value == "external":
                poc_tenant_vars['tenant']['external_subnets'].append(subnet)
            else:
                poc_tenant_vars['tenant']['private_subnets'].append(subnet)
        counter += 1

    poc_tenant_vars['tenant']['protocol'] = poc_tenant['B15'].value
    poc_tenant_vars['tenant'][101]['router_id'] = poc_tenant['B16'].value
    poc_tenant_vars['tenant'][102]['router_id'] = poc_tenant['B21'].value
    poc_tenant_vars['tenant'][101]['r_address'] = poc_tenant['B17'].value
    poc_tenant_vars['tenant'][102]['r_address'] = poc_tenant['B22'].value
    poc_tenant_vars['tenant'][101]['encap'] = poc_tenant['B18'].value
    poc_tenant_vars['tenant'][102]['encap'] = poc_tenant['B23'].value



    if poc_tenant_vars['tenant']['protocol'] == 'OSPF':
        poc_tenant_vars['tenant']['ospf']['area_id'] = poc_tenant['B28'].value
        poc_tenant_vars['tenant']['ospf']['area_type'] = poc_tenant['B29'].value
    elif poc_tenant_vars['tenant']['protocol'] == 'EIGRP':
        poc_tenant_vars['tenant']['eigrp']['as'] = poc_tenant['B32'].value
    elif poc_tenant_vars['tenant']['protocol'] == 'Static':
        poc_tenant_vars['tenant'][101]['static_prefix'] = poc_tenant['B36'].value
        poc_tenant_vars['tenant'][101]['static_nexthop'] = poc_tenant['C36'].value
        poc_tenant_vars['tenant'][102]['static_prefix'] = poc_tenant['B37'].value
        poc_tenant_vars['tenant'][102]['static_nexthop'] = poc_tenant['C37'].value


    return poc_tenant_vars

def saveYAML(var):
    with open('acibootstrap/files/vars/acibootstrap_vars.yml', 'w') as outfile:
        yaml.safe_dump(var, outfile, default_flow_style=False)

def mergeDicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def importvars():
    workbook = openpyxl.load_workbook("acibootstrap/files/vars/acibootstrap.xlsx", data_only=True)

    sys.stderr.write(str(workbook.sheetnames))

    fabric_pol = workbook["fabric_pol"]
    vcenter = workbook["vcenter"]
    poc_tenant = workbook["poc_tenant"]
    mgmt = workbook["mgmt"]

    sys.stderr.write("\nfabric fabric_pol_vars\n")
    fabric_pol_vars = getFabricPolicyVariables(fabric_pol)
    sys.stderr.write("\nreading poc tenant vars\n")
    poc_tenant_vars = getPocTenantVariables(poc_tenant)
    sys.stderr.write("\nreading vmm vars\n")
    vmm_vars = getVMMVars(vcenter)
    sys.stderr.write("\nreading mgmt vars\n")
    mgmt_vars = getMGMTVars(mgmt)

    sys.stderr.write("\nmerging dictionaries\n")
    a = mergeDicts(fabric_pol_vars, poc_tenant_vars)
    b = mergeDicts(a, vmm_vars)
    c = mergeDicts(b, mgmt_vars)

    sys.stderr.write("\nsaving variables to YAML file\n")
    saveYAML(c)
