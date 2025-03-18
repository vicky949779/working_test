import pprint
import re
import os

hostname_pattern = re.compile(r'(\w+)\#')
Port_number = re.compile(r'(\w+)(\d\/\d\/\d)')
lldp_neighbour = re.compile(r'\w+[\w\-\_]\w+)\ +(([\w]+)\ ([\d\/]+))\s.*?(([\w]+)\ ([\d\/]+)')

new_cmd = ["show ip interface brief"]

os.chdir('05_Regex/test_working/backup')

show_lldp_neighbors = ''' C9300# show lldp neighbors
Capability codes:
(R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
(W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other
Device ID          Local Intf     Hold-time  Capability    Port ID
C9500-Core        Ten 1/0/1      120        B R           Ten 1/0/48
C9200-Access1     Gig 1/0/2              Gig 1/0/1
AP-3802           Gig 1/0/3      100        W             Gig 0
IPPhone-8841      Gig 1/0/4      130        T             Gig 0/1
IPPhone8841      Gig 1/0/4      130        T sdfgh            Gig 0/1
Total entries displayed: 4'''

show_interfaces_status = ''' Switch# show interfaces status
Port      Name               Status       Vlan       Duplex  Speed  Type
Gi1/0/1   Uplink to Router   connected    trunk      full    1000   10/100/1000BaseTX
Gi1/0/2   Uplink to Switch   connected    trunk      full    1000   10/100/1000BaseTX
Gi1/0/3   Workstation 1      connected    10         full    1000   10/100/1000BaseTX
Gi1/0/4   Workstation 2      notconnect   20         auto    auto   10/100/1000BaseTX'''


print('######## Parse Formate ############')  
    
# int_iter = int_pattern.finditer(output)
# int_list =list()
# for intf in int_iter:
#     int_dict = dict()
#     int_dict['Interface_name'] = intf.group(1)
#     int_dict['IP_address'] = intf.group(2)
#     int_dict['Staus'] = intf.group(4)
#     int_list.append(int_dict)
# pprint(int_list)

D_L_P_details = lldp_neighbour.finditer(show_lldp_neighbors)
port_details = Port_number.finditer(show_interfaces_status)
host_details = hostname_pattern.finditer(show_interfaces_status)
int_list = list()

for intf in D_L_P_details:
    int_dict = dict()
    int_dict['Device_Id'] = intf.group(1)
    int_dict['Current_device_port'] = intf.group(2)
    int_dict['Neighbour_connected_port'] = intf.group(5)
    int_list.append(int_dict)
pprint(int_list)