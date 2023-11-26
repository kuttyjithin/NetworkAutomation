#Libary required to run this functions
from netmiko import ConnectHandler
import datetime
import fortinetbackup
import scanSubnet

# Function to backup configuration for devices in the given subnet
def backup(subnet, username, password):
    try:
        subnet = subnet.strip()
        print('\nBacking up')

        # 'scanSubnet' is a module or function that scans the subnet and returns a list of devices
        device_list = scanSubnet.scan(subnet)

        #Loops Each devices on the devie list
        for device in device_list:
            cisco_881 = {
                'device_type': 'cisco_ios',
                'host': device,
                'username': username,
                'password': password,
            }
            net_connect = ConnectHandler(**cisco_881)

            # Get the current date and time for the backup file
            time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            
            # Extract the hostname from the device configuration
            hostname = net_connect.send_command('show run | include hostname')
            hostname = hostname.strip().split("hostname ")[-1]

            # Define the backup file name
            filename = "backups\\" + hostname + "-backup-" + time + ".txt"
            filename2 = "backups\\" + hostname + ".txt"

            print("**********************************\n")
            print("Backing UP " + hostname)
            print("\n**********************************")

            # Get and save the device's configuration
            backup_config = net_connect.send_command('show run')
            
            with open(filename, 'w') as backup:
                backup.write(backup_config + "\n\n")
            with open(filename2, 'w') as backup:
                backup.write(backup_config + "\n\n")

        # Assuming 'fortinetbackup.fortinetbackup()' is a function to backup Fortinet devices
        fortinetbackup.fortinetbackup()
    except:
        print("error")

# Main function
def main():
    Prog_Name = """\tLab#2 - Student Assignment 1 - A. Created by Jithin Jose. Written on 9/30/2023
    *****************************************************************************
    NETW3100 Fall 2023
    This program validates the IP address and Subnet Based on User Input and scans the subnet range
    *****************************************************************************
    """
    print(Prog_Name)

    try:
        subnet = input("Enter the Management subnet to scan (e.g., 192.168.1.0/24): ")
        subnet = subnet.strip()
        print('\nBacking up')
        backup(subnet, "cisco", "cisco")

    except:
        print("an error has occurred")

if __name__ == "__main__":
    main()
