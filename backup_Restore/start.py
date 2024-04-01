# Import necessary libraries
from nornir import InitNornir  # Importing Nornir for network automation
import json  # For handling JSON data
from nornir_netmiko import netmiko_send_command  # For sending Netmiko commands through Nornir
from nornir_utils.plugins.functions import print_result  # Utility for printing Nornir results
from netmiko import ConnectHandler  # For establishing SSH connections using Netmiko
import time  # For tracking execution time

# Function using Nornir to run commands on devices
def nornir():
    try:
        start_time = time.time()  # Record the start time
        nr = InitNornir("nornir_lab03/config.yaml")  # Initialize Nornir with a config file
        # Run Netmiko command "Show ip int br" on devices using Nornir
        result = nr.run(task=netmiko_send_command, command_string="Show ip int br", use_textfsm=True)
        print("\n----------------------Nornir Output---------------------\n")
        print_result(result)  # Print the result obtained from Nornir
        print("\n----------------------Nornir Output---------------------\n")

        end_time = time.time()  # Record the end time
        total_time = str(end_time - start_time)  # Calculate the total time taken
        return total_time  # Return the total time taken as a string

    except Exception as e:
        print(f"Error occurred: {e}")

# Function using Netmiko directly to run commands on devices
def netmiko():
    try:
        filepath = "C:\\Users\\Jithin Jose\\OneDrive - NAIT\\BAITS\\NETW3100\\NETW3100\\devices.json"
        with open('devices.json', 'r') as json_file:
            json_python = json.load(json_file)
        print("\n----------------------Netmiko Output---------------------\n")
        start_time = time.time()  # Record the start time
        for devices in json_python:
            for device in devices:
                device_type = devices[device]['device_type']
                cisco_881 = {
                    'device_type': devices[device]['device_type'],
                    'host': devices[device]['host'],
                    'username': devices[device]['username'],
                    'password': devices[device]['password'],
                }
                # Connect to the device using Netmiko
                net_connect = ConnectHandler(**cisco_881)
                output = net_connect.send_command('show ip int br', use_textfsm=True)
                print(output)  # Print the command output obtained from Netmiko
        end_time = time.time()  # Record the end time
        print("\n----------------------Netmiko Output---------------------\n")
        total_time = str(end_time - start_time)  # Calculate the total time taken
        return total_time  # Return the total time taken as a string

    except Exception as e:
        print(f"Error occurred: {e}")

# Main function to compare execution time between Nornir and Netmiko
def main():
    try:
        nornir_time = float(nornir())  # Execute Nornir function and get the time taken
        netmiko_time = float(netmiko())  # Execute Netmiko function and get the time taken
        print("Nornir Time:", nornir_time)  # Print Nornir execution time
        print("Netmiko Time:", netmiko_time)  # Print Netmiko execution time
        print("Time Difference:", netmiko_time - nornir_time)  # Print the time difference between Netmiko and Nornir

    except Exception as e:
        print("Error:", e)

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
