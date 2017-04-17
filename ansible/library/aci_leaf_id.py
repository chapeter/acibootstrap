#!/usr/local/bin/python

# Copyright 2015 Jason Edelman <jason@networktocode.com>
# Network to Code, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---

module: aci_rest
short_description: Direct access to the APIC API
description:
    - Offers direct access to the APIC API
author: Jason Edelman (@jedelman8)
requirements:
    - ACI Fabric 1.0(3f)+
    - Cobra SDK
notes:
    - Tenant must be exist prior to using this module
options:
    uri:
        description:
            - uri being used to execute API calls. Must end in .xml or .json
        required: true
        default: null
        choices: []
        aliases: []
    action:
        description:
            - http verb, i.e. post or get
        required: true
        default: null
        choices: ['post', 'get']
        aliases: []
    config_file:
        description:
            - name of the absolute path of the filname that includes the body
              of the http request being sent to the ACI fabric
        required: false
        default: null
        choices: []
        aliases: []
    host:
        description:
            - IP Address or hostname of APIC resolvable by Ansible control host
        required: true
        default: null
        choices: []
        aliases: []
    username:
        description:
            - Username used to login to the switch
        required: true
        default: 'admin'
        choices: []
        aliases: []
    password:
        description:
            - Password used to login to the switch
        required: true
        default: 'C1sco12345'
        choices: []
        aliases: []
    protocol:
        description:
            - Dictates connection protocol to use
        required: false
        default: https
        choices: ['http', 'https']
        aliases: []
'''

EXAMPLES = '''

# add a tenant
- aci_rest: action=post uri=/api/mo/uni.xml config_file=/home/cisco/ansible/aci/configs/aci_config.xml host={{ inventory_hostname }} username={{ user }} password={{ pass }}

# get tenants
- aci_rest: action=get uri=/api/node/class/fvTenant.json host={{ inventory_hostname }} username={{ user }} password={{ pass }}

# configure contracts
- aci_rest: action=post uri=/api/mo/uni.xml config_file=/home/cisco/ansible/aci/configs/contract_config.xml host={{ inventory_hostname }} username={{ user }} password={{ pass }}

'''
import socket
import json
import requests


def main():

    module = AnsibleModule(
        argument_spec=dict(
            config_file=dict(),
            host=dict(required=True),
            username=dict(type='str', default='admin'),
            password=dict(type='str', default='cisco123'),
            protocol=dict(choices=['http', 'https'], default='http')
        ),
        supports_check_mode=False
    )

    username = module.params['username']
    password = module.params['password']
    protocol = module.params['protocol']
    host = socket.gethostbyname(module.params['host'])

    uri = '/api/node/class/fabricNode.json?query-target-filter=and(eq(fabricNode.role,"leaf"))'
    config_file = module.params['config_file']
    file_exists = False
    if config_file:
        if os.path.isfile(config_file):
            file_exists = True
        else:
            module.fail_json(msg='Cannot find/access config_file:\n{0}'.format(
                config_file))

    apic = '{0}://{1}/'.format(protocol, host)

    auth = dict(aaaUser=dict(attributes=dict(name=username, pwd=password)))

    url = apic + 'api/aaaLogin.json'

    authenticate = requests.post(url, data=json.dumps(auth),
                                 timeout=2, verify=False)

    if authenticate.status_code != 200:
        module.fail_json(msg='could not authenticate to apic',
                         status=authenticate.status_code,
                         response=authenticate.text)

    if uri.startswith('/'):
        uri = uri[1:]
    url = apic + uri

    if file_exists:
        with open(config_file, 'r') as config_object:
                config = config_object.read()
    else:
        config = None


    req = requests.get(url, cookies=authenticate.cookies,
                           data=config, verify=False)

    response = req.json()
    response = response['imdata']

    switchlist = []

    for switch in response:
        switchid = switch['fabricNode']['attributes']['id']
        switchlist.append(switchid)

    status = req.status_code


    results = {}
    results['status'] = status
    results['response'] = switchlist

    module.exit_json(**results)

from ansible.module_utils.basic import *
main()
