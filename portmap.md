# Port Layout for acibootstrap

This document is intended to provide a layout of they physical ports to be used for acibootstrap.

We are assuming two leaf switches with 48 ports.  If you have more than two, those extra leafs will not have their physical ports configured by acibootstrap or your leafs have more than 48 ports, those ports will not be configured beyond port 48


* [ ] .
* [ ] .

## Ports
| complete | port | device | info | related items |
|:---:|:---:|---|---| --- |
|x| 1 | l2-out| |
|x| 2 | L3-out| Speed Defined in XLSX|
|| 3 | L2/L3-Out | User-defined|
|| 4 | L2/L3-Out | User-defined|
|| 5 | L2/L3-Out | User-defined|
|| 6 | L2/L3-Out | User-defined|
|| 7 | L2/L3-Out | User-defined|
|| 8 | L2/L3-Out | User-defined|
|| 9 | L2/L3-Out | User-defined|
|| 10 | Network Services| User-defined|
|| 11 | Network Services| User-defined|
|| 12 | Network Services| User-defined|
|| 13 | Network Services| User-defined|
|| 14 | Network Services| User-defined|
|| 15 | Network Services| User-defined|
|| 16 | DNS/AD/LDAP/DHCP/etc.| Common |
|| 17 | DNS/AD/LDAP/DHCP/etc.| Common |
|| 18 | DNS/AD/LDAP/DHCP/etc.| Common |
|| 19 | DNS/AD/LDAP/DHCP/etc.| Common |
|x| 20 | UCS-FI A| vpc-1 |
|x| 21 | UCS-FI A| vpc-1 |
|x| 22 | UCS-FI B| vpc-2 |
|x| 23 | UCS-FI B| vpc-2|
|| 24 | | |
|| 25 | | |
|| 26 | | |
|| 27 | | |
|| 28 | | |
|| 29 | | |
|x| 30 | Rack Servers | 10g vpc |
|x| 31 | Rack Servers | 10g vpc |
|x| 32 | Rack Servers | 10g vpc |
|x| 33 | Rack Servers | 10g vpc |
|x| 34 | Rack Servers | 1g vpc |
|x| 35 | Rack Servers | 1g vpc |
|x| 36 | Rack Servers | 1g vpc |
|x| 37 | Rack Servers | 1g vpc |
|x| 38 | Rack Servers | 1g vpc |
|x| 39 | Rack Servers | 10g |
|x| 40 | Rack Servers | 10g |
|x| 41 | Rack Servers | 10g |
|x| 42 | Rack Servers | 1g |
|x| 43 | Rack Servers | 1g |
|x| 44 | Rack Servers | 1g |
|x| 45 | Rack Servers | 1g |
|| 46 | apic-3 | |
|| 47 | apic-2 | |
|| 48 | apic-1 | |

## Pools
| Pool | VLANS | info |
|:---:|---|---|
| VMM | 2000 - 2099 | vlans used for VDS integration |
| esxi | 2100 - 2109 | Vlans used for BM |
| L3 router | 2110 - 2119 | VLANs used for L3 outs |
| L2 out | 2120 - 2129 | VLANs used for L2 outs |
