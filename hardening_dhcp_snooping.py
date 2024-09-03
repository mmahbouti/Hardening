from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint


def dhcp_snooping(connection):
    # Show command that we execute.
    command1 = "show vlan brief"
    command2 = "show interfaces status"
    
    output1 = connection.send_command(command1,use_textfsm=True)
    output2 = connection.send_command(command2,use_textfsm=True)

    vlan_id_list_for_dhcp_snooping=[]
    for e in output1:
        vlan_id = e["vlan_id"]
        #remove default vlan and WIFI-VLAN and VOIP and WLC
        if vlan_id != '1002' and vlan_id != '1003' and vlan_id != '1004' and vlan_id != '1005' and vlan_id != '101' and vlan_id != '102' and vlan_id != '103' and vlan_id != '104'and vlan_id != '402':
            vlan_id_list_for_dhcp_snooping.append(vlan_id)

    # Convert the list of string to a comma-separated string
    temp = [int(i) for i in vlan_id_list_for_dhcp_snooping]
    vlan_id_string = ",".join(map(str, temp))


    ip_dhcp_snooping_command_vlan = "ip dhcp snooping vlan " + str(vlan_id_string)
    #print(ip_dhcp_snooping_command_vlan)
    #ip_arp_inspection_command = "ip arp inspection vlan " + str(vlan_id_string)

    static_config_for_dhcp_snooping_global = ["ip dhcp snooping",ip_dhcp_snooping_command_vlan]


    trunk_interfaces=[]
    for e in output2:
        if e["vlan_id"] == "trunk":
            trunk_interfaces.append(e["port"])

    static_config_for_trunk_port = ["ip dhcp snooping trust","logging event link-status",'exit']


    config_trunk_ports = []

    for e in trunk_interfaces:
        interface_name = "interface " + str(e) 
        config_trunk_ports.append(interface_name)
        config_trunk_ports = config_trunk_ports + static_config_for_trunk_port


    result = static_config_for_dhcp_snooping_global + config_trunk_ports

    return result

