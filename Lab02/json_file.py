from netmiko import ConnectHandler
from ping3 import ping
import json

def get_username_password():
    username = input("Enter the SSH username: ")
    password = input("Enter the SSH password: ")
    return username, password

def connect_device(device_type, ip_address, username, password):
    while True:
        try:
            device = {
                'device_type': device_type,
                'ip': ip_address,
                'username': username,
                'password': password,
            }
            net_connect = ConnectHandler(**device)
            return net_connect
        except Exception as e:
            print(f"Error connecting to {device_type} at {ip_address}: {e}")
            retry = input("Do you want to retry with a different password or cancel (r/c)? ")
            if retry.lower() == 'c':
                return None
            username = input("Enter Userame: ")
            password = input("Enter the new password: ")

def scan(subnet, username, password):
    try:
        print("""
              *************************************
              Creating JSON File Active Devices
              *************************************""")
        ip_address_octets = subnet.split(".")
        device_list = {}  # Create an empty dictionary to store device dictionaries

        for i in range(1, 20):
            ip_to_scan = f"{ip_address_octets[0]}.{ip_address_octets[1]}.{ip_address_octets[2]}.{i}"
            response_time = ping(ip_to_scan, timeout=1)

            if response_time is not None:
                device_info = None
                net_connect = None

                # First, try connecting as Cisco
                net_connect = connect_device('cisco_ios', ip_to_scan, username, password)

                if net_connect:
                    try:
                        hostname = net_connect.send_command('show run | include hostname')
                        interfaces_output = net_connect.send_command('show ip interface brief')
                        device_type1 = net_connect.send_command('show version')
                        net_connect.disconnect()

                        # Extract relevant interface information
                        interfaces_info = ""
                        for line in interfaces_output.splitlines():
                            if ip_to_scan in line:
                                interfaces_info = line.split()[0]
                        parts = device_type1.split(' ', 2)
                        device_type = parts[:2]
                        result_device = '_'.join(device_type)
                        result_device = result_device.lower()
                        result_device = result_device.lower()
                        if result_device == "cisco_nexus":
                            result_device = 'cisco_ios'

                        device_info = {
                            'device type': result_device,
                            'Host': ip_to_scan,
                            'hostname': hostname.strip().split("hostname ")[-1],
                            'interfaces_output': interfaces_info,
                            'Username': username,  # Use the provided username
                            'Password': password  # Use the provided password
                        }
                    except:  # Replace SpecificException with the actual exception you want to exempt
                        print("Handled SpecificException")
                        # Handle the specific exception here

                # For Fortinet devices, handle password prompts
                if net_connect and 'cisco' not in device_info.get('device type', ''):
                    print("Connected as Fortinet, need username and password")
                    while True:
                        fortinet_username = input("Confirm Fortinet username (or 'c' to cancel): ")
                        if fortinet_username.lower() == 'c':
                            break
                        fortinet_password = input("Confirm Fortinet password (or 'c' to cancel): ")
                        if fortinet_password.lower() == 'c':
                            break
                        net_connect = connect_device('fortinet', ip_to_scan, fortinet_username, fortinet_password)
                        if net_connect:
                            # Use the 'show system global' command to retrieve the hostname
                            hostname_output = net_connect.send_command('show system global')
                            hostname_lines = hostname_output.splitlines()
                            
                            hostname = 'N/A'  # Default value if not found
                            for line in hostname_lines:
                                if line.strip().startswith("set hostname"):
                                    parts = line.split('set hostname')[1].strip()
                                    hostname = parts.strip('"')
                            interface_output = net_connect.send_command('show system interface')
                            interface_lines = interface_output.splitlines()
                           # Initialize variables to store the interface information
                            interface_info = []
                            found_ip = False

                            # Loop through the interface lines
                            for line in interface_lines:
                                if ip_to_scan in line:
                                    # We found the IP address, capture the two lines before it
                                    index = interface_lines.index(line)
                                    if index >= 2:
                                        # Add the second line before the IP
                                        interface_info.append(interface_lines[index - 2])
                                       
                                    break

                            # Combine the lines in the interface_info list into a single string
                            interface_info = str(interface_info)
                            parts = interface_info.split("edit", 1)

                            # If there's something after "edit," it will be in parts[1]. You can strip any leading and trailing whitespace.
                            if len(parts) > 1:
                                result = parts[1].strip()
                            else:
                                result = ''   
                            interface_info = result 
                            interface_info = interface_info.strip('"\']')                      

                            device_info = {
                                'device type': 'fortinet',
                                'Host': ip_to_scan,
                                'hostname': hostname,
                                'interfaces_output': interface_info,
                                'Username': fortinet_username,
                                'Password': fortinet_password
                            }
                            net_connect.disconnect()
                            break

                if device_info:
                    device_list[device_info['hostname']] = device_info  # Use the hostname as the dictionary key

        with open("devices.json", "w") as jsonfile:
            json.dump(device_list, jsonfile, indent=4)  # Save the dictionary of device dictionaries

        print("Device List:")
        print(json.dumps(device_list, indent=4))

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    try:
        subnet = input("Enter the Management subnet to scan (e.g., 192.168.1.0/24): ")

        subnet = subnet.strip()
        username, password = get_username_password()  # Get the username and password from the user
        scan(subnet, username, password)  # Pass the username and password to the scan function
    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == "__main__":
    main()
