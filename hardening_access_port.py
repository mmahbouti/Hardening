from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint


def hardening_access_port(connection):

    command = "show interfaces status"
    #with ConnectHandler(**connection) as net_connect:
    output = connection.send_command(command,use_textfsm=True)

    access_interfaces=[]

    for e in output:
        if e["vlan_id"] != "trunk":
            access_interfaces.append(e["port"])


    static_config_for_access_port = ["switchport host","switchport port-security","switchport port-security maximum 10","switchport port-security violation shutdown"
    ,"switchport port-security mac-address sticky","spanning-tree bpduguard enable","spanning-tree bpdufilter enable","storm-control broadcast level 50.00"
    ,"storm-control multicast level 35.00","logging event link-status","logging event port-security","ip dhcp snooping limit rate 10",'exit']


    config_access_ports = []

    for e in access_interfaces:
        interface_name = "interface " + str(e) 
        config_access_ports.append(interface_name)
        config_access_ports = config_access_ports + static_config_for_access_port

    return(config_access_ports)

