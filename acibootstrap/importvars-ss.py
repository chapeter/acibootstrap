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
    with open('files/vars/acibootstrap_vars_ss.yml', 'w') as outfile:
        yaml.safe_dump(var, outfile, default_flow_style=False)

def mergeDicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def buildTenantVars(raw_vars, key_list):

    tn_list = []
    #build list of tenant_name_x keys that contain a value
    for key in raw_vars:
            #Find key
            if key.startswith('tenant_name_'):
                #check to see if tenant name was filled out
                if raw_vars[key] != None:
                    tn_list.append(key)

    #Gather Tenant variables

    tn_data = []
    for tn in tn_list:
        tn_dict = {}
        #Get the data into a list and remove the _x
        for key in key_list:
            tn_dict[(key + tn[-1])[:-2]] = raw_vars[key + tn[-1]]

        external_subnets = []
        internal_subnets = []
        tn_dict[201] = {'encap': int(tn_dict['vlan_id']), 'r_address':tn_dict['leaf201_routed_addr'], 'router_id':tn_dict['leaf201_routed_addr']}
        tn_dict[202] =  {'encap': int(tn_dict['vlan_id']), 'r_address':tn_dict['leaf202_routed_addr'], 'router_id':tn_dict['leaf202_routed_addr']}
        tn_dict['eigrp'] = {}
        tn_dict['ospf'] = {}
        tn_dict['static'] = {}
        tn_dict['protocol'] = tn_dict['routed_out_protocol'].upper()
        print(tn_dict)
        for key in tn_dict:
            if str(key).endswith('_subnet'):
                if tn_dict[key] != None:
                    network_name = key[:-7]
                    network_type = tn_dict[network_name+'_type']
                    network_address = tn_dict[key]
                    print(network_name, network_type, network_address)
                    if network_type == 'external':
                        external_subnets.append({'address': network_address, 'name': network_name})
                    elif network_type == 'private':
                        internal_subnets.append({'address': network_address, 'name': network_name})

        if tn_dict['protocol'] == 'OSPF':
            tn_dict['ospf'] = {'area_id':int(tn_dict['ospf_id']), 'area_type':tn_dict['ospf_area_type']}
        elif tn_dict['protocol'] == 'EIGRP':
            tn_dict['eigrp'] = {'as':int(tn_dict['eigrp_pid'])}

        tn_dict['name'] = tn_dict['tenant_name']
        tn_dict['external_subnets'] = external_subnets
        tn_dict['internal_subnets'] = internal_subnets
        #clean up data
        #Found from https://stackoverflow.com/questions/4653626/python-dictionary-remove-all-the-keys-that-begins-with-s/4653641#4653641?newreg=49dd7382783d4591b79bf1cd9e8f8645
        for k in list(tn_dict.keys()):
          if str(k).startswith('ntwk') or str(k).endswith('_routed_addr') or str(k).startswith('vlan') or str(k).startswith('routed_out_') or str(k).startswith('ospf_') or str(k).startswith('eigrp_'):
            tn_dict.pop(k)
        tn_data.append(tn_dict)

    return tn_data

def scrapeSheet(var_sheet):
    raw_vars = {}
    for col in var_sheet.columns:
        raw_vars[col[0].value] = col[1].value

    return raw_vars

def importvars_ss():
    workbook = openpyxl.load_workbook("files/vars/ACI-Bootstrap-Tool.xlsx", data_only=True)
    var_sheet = workbook['ACI-Bootstrap-Tool']
    raw_vars = scrapeSheet(var_sheet)

    tn_key_list = ['leaf201_routed_addr_','leaf202_routed_addr_','ntwk_one_subnet_','ntwk_one_type_','ntwk_two_subnet_','ntwk_two_type_','ntwk_three_subnet_','ntwk_three_type_','ntwk_four_type_','ntwk_four_subnet_','ospf_area_type_','ospf_id_','routed_out_protocol_','vlan_id_','eigrp_pid_', 'tenant_name_']

    tenant_vars = buildTenantVars(raw_vars, tn_key_list)


    print(tenant_vars)
    raw_vars['tenant'] = tenant_vars


    #Clean up data
    raw_vars['bgp_as'] = int(raw_vars['bgp_as'])
    raw_vars['oob_from'] = raw_vars['switch_oob_pool_beg']
    raw_vars['oob_to'] = raw_vars['switch_oob_pool_end']
    raw_vars['oob_gw'] = raw_vars['switch_oob_pool_gateway']
    raw_vars['vcenter_dc'] = raw_vars['vcenter_datacenter']
    raw_vars['vmmpool_start'] = int(raw_vars['vmm_vlan_pool_start'])
    raw_vars['vmmpool_end'] = int(raw_vars['vmm_vlan_pool_end'])
    for k in list(raw_vars.keys()):
      if k.startswith(tuple(tn_key_list)) or k.startswith('switch_oob_pool_') or k.startswith('vcenter_datacenter') or k.startswith('vmm_'):
        raw_vars.pop(k)


    saveYAML(raw_vars)

importvars()
