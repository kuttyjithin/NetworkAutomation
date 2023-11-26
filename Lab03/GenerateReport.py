# Import necessary libraries
import napalm  # Unused import
import json  # For handling JSON data
import csv  # For handling CSV files
from netmiko import ConnectHandler  # For SSH connections to network devices

# Define a function named 'info'
def info():
    # Read devices' information from a JSON file named 'devices.json'
    with open('devices.json', 'r') as json_file:
        json_python = json.load(json_file)  # Load JSON data into a Python dictionary

    # Define CSV header outside the loop
    Report_Headers = ['hostname', 'MAC', 'type', 'serial', 'image', 'os_ver', 'os', 'hardware', 'uptime']

    # Write CSV header once before the loop
    with open('Device_netmiko_report.csv', 'w') as file:
        writer = csv.DictWriter(file, Report_Headers)
        writer.writeheader()  # Write CSV header using the defined headers

    # Iterate through devices in the JSON data
    for device_info in json_python:
        for device_name, device_data in device_info.items():
            # Extract device information from the JSON data
            device_type = device_data['device_type']
            cisco_881 = {
                'device_type': device_data['device_type'],
                'host': device_data['host'],
                'username': device_data['username'],
                'password': device_data['password'],
            }

            # Connect to the device using Netmiko
            net_connect = ConnectHandler(**cisco_881)
            output = net_connect.send_command('show ver', use_textfsm=True)  # Send command to retrieve device info
            print(output)  # Print the output (optional)

            # Extract specific information from the command output
            hostname = output[0]['hostname']
            MAC = output[0]['mac_address']
            type = output[0]['hardware'][0]
            serial = output[0]['serial'][0]
            image = output[0]['running_image']
            os_ver = output[0]['version']
            os = output[0]['rommon']
            hardware = output[0]['hardware'][0]
            up = output[0]['uptime']

            # Write device information to the CSV file
            with open('Device_netmiko_report.csv', 'a') as file:
                writer = csv.DictWriter(file, Report_Headers)
                writer.writerow({
                    'hostname': hostname, 'MAC': MAC, 'type': type, 'serial': serial,
                    'image': image, 'os_ver': os_ver, 'os': os, 'hardware': hardware, 'uptime': up
                })

            # Print a message confirming report generation for a specific hostname
            print(f"Report has been generated for {hostname}")

# Run the 'info' function if this script is executed directly
if __name__ == "__main__":
    info()
