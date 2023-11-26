from netmiko import ConnectHandler
import datetime
from ping3 import ping
import json
import datetime
import scanSubnet
import fortinetestore

#this functions restores teh backup
def restore(subnet , username, password):
    try:
        subnet =subnet.strip()
        print('\nRestoring')
        device_list =scanSubnet.scan(subnet)
        
        #Loops each devices in the device
        for devices in device_list:
            cisco_881 = {
            'device_type': 'cisco_ios',
            'host':   devices,
            'username':username,
            'password':password,
            }
            #Connect into the Device
            net_connect = ConnectHandler(**cisco_881)

            #Getting the hostname and grabing the fie format for the restre files
            hostname = net_connect.send_command('show run | include hostname')
            hostname=hostname.strip().split("hostname ")[-1]
            restore_file="backups\\"+hostname+".txt"
            print(restore_file)
            
            #Opens the restore file and adds the command to the networking device.
            with open(restore_file, 'r') as file_lines:
                command= file_lines.read().splitlines()
            
                print("**********************************\n")
                print("Restoring " + hostname)
                print("\n**********************************")
                input = net_connect.send_config_set(command)
                print(input)


        #Restore the fortinet device
        fortinetestore.fortinetRestore()

     
    except Exception as e:
        print(f"an error has occured{e}")

def main():
    Prog_Name = """\tLab#2 - Student Assignment  1 -A . Created by Jithin Jose.  Written on 9/30/2023
    *****************************************************************************
    NETW3100 Fall 2023
    This program validate the IP address and Subnet Based on User Input and scan the subnet range
    *****************************************************************************
    """
    print (Prog_Name)


    #Check the main program.
    try:
            subnet = input("Enter the Managment subnet to Restore (e.g., 192.168.1.0/24): ")
            subnet =subnet.strip()
            print('\nRestoring')
            restore(subnet ,"cisco" ,"cisco")
    
    except:
        print("an error has occured")
        
if __name__=="__main__":

    main()
