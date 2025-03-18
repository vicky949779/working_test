import pprint
import re
import os

# Corrected regex patterns
hostname_pattern = re.compile(r'([a-zA-Z0-9\-]+)#')
Port_number = re.compile(r'\w+(\d\/\d\/\d+)')
lldp_neighbour = re.compile(r'(\w+[\w\-\_]\w+)\s+([\w]+)\s([\d\/]+)\s.*?([\w]+)\s([\d\/]+)')

# Sample input data
show_lldp_neighbors = ''' Cat9600# show lldp neighbors
Capability codes:
(R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
(W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other

Device ID          Local Intf     Hold-time  Capability    Port ID
C9500-Core        Ten 1/0/1      120        B R           Ten 1/0/48
C9300-Access1     Gig 1/0/2      110        B R           Gig 1/0/1
AP-4800           Gig 1/0/3      100        W             Gig 0
IPPhone-8861      Gig 1/0/4      130        T             Gig 0/1
IPPhone8861       Gig 1/0/4      130        T             Gig 0/1

Total entries displayed: 5
'''

show_interfaces_status = ''' Cat9600# show ip interface brief

Interface                   IP-Address      OK? Method Status                Protocol
GigabitEthernet1/0/1        192.168.1.1     YES manual up                    up
GigabitEthernet1/0/2        unassigned      YES unset  administratively down down
GigabitEthernet1/0/3        unassigned      YES unset  up                    up
GigabitEthernet1/0/4        unassigned      YES unset  up                    up
GigabitEthernet1/0/5        unassigned      YES unset  up                    up
GigabitEthernet1/0/6        unassigned      YES unset  up                    up
GigabitEthernet1/0/7        unassigned      YES unset  administratively down down
GigabitEthernet1/0/8        unassigned      YES unset  up                    up
GigabitEthernet1/0/9        unassigned      YES unset  up                    up
GigabitEthernet1/0/10       unassigned      YES unset  administratively down down
GigabitEthernet1/0/11       unassigned      YES unset  up                    up
GigabitEthernet1/0/12       unassigned      YES unset  up                    up
GigabitEthernet1/0/13       unassigned      YES unset  administratively down down
GigabitEthernet1/0/14       unassigned      YES unset  up                    up
GigabitEthernet1/0/15       unassigned      YES unset  up                    up
GigabitEthernet1/0/16       unassigned      YES unset  administratively down down
GigabitEthernet1/0/17       unassigned      YES unset  up                    up
GigabitEthernet1/0/18       unassigned      YES unset  up                    up
GigabitEthernet1/0/19       unassigned      YES unset  administratively down down
GigabitEthernet1/0/20       unassigned      YES unset  up                    up
GigabitEthernet1/0/21       unassigned      YES unset  up                    up
GigabitEthernet1/0/22       unassigned      YES unset  administratively down down
GigabitEthernet1/0/23       unassigned      YES unset  up                    up
GigabitEthernet1/0/24       unassigned      YES unset  up                    up
GigabitEthernet1/0/25       unassigned      YES unset  administratively down down
GigabitEthernet1/0/26       unassigned      YES unset  up                    up
GigabitEthernet1/0/27       unassigned      YES unset  up                    up
GigabitEthernet1/0/28       unassigned      YES unset  administratively down down
GigabitEthernet1/0/29       unassigned      YES unset  up                    up
GigabitEthernet1/0/30       unassigned      YES unset  up                    up
GigabitEthernet1/0/31       unassigned      YES unset  administratively down down
GigabitEthernet1/0/32       unassigned      YES unset  up                    up
GigabitEthernet1/0/33       unassigned      YES unset  up                    up
GigabitEthernet1/0/34       unassigned      YES unset  administratively down down
GigabitEthernet1/0/35       unassigned      YES unset  up                    up
GigabitEthernet1/0/36       unassigned      YES unset  up                    up
GigabitEthernet1/0/37       unassigned      YES unset  administratively down down
GigabitEthernet1/0/38       unassigned      YES unset  up                    up
GigabitEthernet1/0/39       unassigned      YES unset  up                    up
GigabitEthernet1/0/40       unassigned      YES unset  administratively down down
GigabitEthernet1/0/41       unassigned      YES unset  up                    up
GigabitEthernet1/0/42       unassigned      YES unset  up                    up
GigabitEthernet1/0/43       unassigned      YES unset  administratively down down
GigabitEthernet1/0/44       unassigned      YES unset  up                    up
GigabitEthernet1/0/45       unassigned      YES unset  up                    up
GigabitEthernet1/0/46       unassigned      YES unset  administratively down down
GigabitEthernet1/0/47       unassigned      YES unset  up                    up
GigabitEthernet1/0/48       unassigned      YES unset  administratively down down
TenGigabitEthernet1/1/1     10.10.10.1      YES manual up                    up
TenGigabitEthernet1/1/2     unassigned      YES unset  up                    up
TenGigabitEthernet1/1/3     unassigned      YES unset  up                    up
TenGigabitEthernet1/1/4     unassigned      YES unset  up                    up
TenGigabitEthernet1/1/5     unassigned      YES unset  administratively down down
TenGigabitEthernet1/1/6     unassigned      YES unset  up                    up
TenGigabitEthernet1/1/7     unassigned      YES unset  up                    up
TenGigabitEthernet1/1/8     unassigned      YES unset  administratively down down
FortyGigabitEthernet1/2/1   unassigned      YES unset  administratively down down
FortyGigabitEthernet1/2/2   192.168.2.1     YES manual up                    up
HundredGigabitEthernet1/3/1 unassigned      YES unset  up                    up
HundredGigabitEthernet1/3/2 unassigned      YES unset  administratively down down
Vlan1                      192.168.1.254   YES manual up                    up
Vlan10                     172.16.10.1     YES manual up                    up
Vlan20                     172.16.20.1     YES manual up                    up

Cat9600#
'''

# Extract details
D_L_P_details = lldp_neighbour.finditer(show_lldp_neighbors)
port_details = Port_number.finditer(show_interfaces_status)
host_details = hostname_pattern.finditer(show_interfaces_status)

# Store extracted details in a list
int_list = []
# for inta in host_details:
#     int_dict = {
#         'Host_name': inta.group(1)
#     }
#     int_list.append(int_dict)

# for intf in D_L_P_details:
#     int_dict = {
#         'Device_Id': intf.group(1),
#         'Current_device_port': intf.group(2) + " " + intf.group(3),
#         'Neighbour_connected_port': intf.group(4) + " " + intf.group(5),
#     }
#     int_list.append(int_dict)

for intb in port_details:
    int_dict = {
        'hostname': intb.group(1),
        'Port_number': intb.group(0)
    }
    int_list.append(int_dict)



pprint.pprint(int_list)


