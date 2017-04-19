# Port Layout for acibootstrap

This document is intended to provide a layout of they physical ports to be used for acibootstrap.

We are assuming two leaf switches with 48 ports.  If you have more than two, those extra leafs will not have their physical ports configured by acibootstrap or your leafs have more than 48 ports, those ports will not be configured beyond port 48

## Ports
| port | device | info | related items |
|:---:|---|---| --- |
| 1 | ucs a| vpc between leaf 1 and 2|
| 2 | ucs b| vpc between leaf 1 and 2|
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |
| 11 | | |
| 12 | | |
| 13 | | |
| 14 | | |
| 15 | | |
| 16 | | |
| 17 | | |
| 18 | | |
| 19 | | |
| 20 | | |
| 21 | | |
| 22 | | |
| 23 | | |
| 24 | | |
| 25 | | |
| 26 | | |
| 27 | | |
| 28 | | |
| 29 | | |
| 30 | l3 out | built via l3 sub interfaces |
| 31 | l2 out | |
| 31 | | |
| 32 | | |
| 33 | | |
| 34 | | |
| 35 | | |
| 36 | | |
| 37 | | |
| 38 | | |
| 39 | | |
| 40 | | |
| 41 | | |
| 42 | | |
| 43 | | |
| 44 | | |
| 45 | | |
| 46 | apic | |
| 47 | apic | |
| 48 | apic | |

## Pools
| Pool | VLANS | info |
|:---:|---|---|
| VMM | 2000 - 2099 | vlans used for VDS integration |
| esxi | 2100 - 2109 | Vlans used for BM |
| L3 router | 2110 - 2119 | VLANs used for L3 outs |
