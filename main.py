from netmiko import ConnectHandler
import hardening_access_port
import hardening_dhcp_snooping
import global_hardening_config
from pprint import pprint
from getpass import getpass


file_name = 'globalconfig.txt'
host_list = ["10.3.13.67","10.3.13.68","10.3.13.69","10.3.13.70","10.3.13.71","10.3.13.72"]
#host_list = ["10.3.13.67","10.3.13.68"]

password = getpass()

for ip in host_list:
    net_connect = ConnectHandler(
        device_type="cisco_ios",
        host=ip,
        username=input("Enter your Username: "),
        password=password,
    )
    output_file_name = str(ip) + ".txt"


    x = hardening_access_port.hardening_access_port(net_connect)
    y = hardening_dhcp_snooping.dhcp_snooping(net_connect)
    z = global_hardening_config.convert_text_to_list(file_name)

    result_list  = x + y + z 

    with open(output_file_name, 'w') as file:
        # Write each item in the list to the file
        for line in result_list:
            file.write(line + '\n')  # Add a newline character after each line

    print("Configuration written to " + str(output_file_name))


