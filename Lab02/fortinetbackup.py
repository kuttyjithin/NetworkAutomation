#Liabary required to run this code
from netmiko import ConnectHandler
import datetime
from ping3 import ping

#Function backups the fortine Switch
def fortinetBackup():
    cisco_881 = {
            'device_type': 'fortinet',
            'host':   '192.168.3.18',
            'username': 'admin',
            'password': 'P@ssw0rd',
            }
    net_connect = ConnectHandler(**cisco_881)
    
    
    #Runs the backup config  
    backup_config  = net_connect.send_command('show')



    # Get the current date and time for the backup file
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Extract the hostname from the device configuration
    hostname = net_connect.send_command('get system status').split('Hostname: ')[1].split('\n')[0]
    
    # Define the BAckup File Name
    filename ="backups\\"+hostname+"-backup-"+time+".txt"
    filename2 ="backups\\"+hostname+".txt"
    print(filename)
    print("**********************************\n")
    print("Backing UP " + hostname)
    print("\n**********************************")
    

    #Functions to write configuration  on the file
    with open(filename,'w') as backup:
        backup.write(backup_config + "\n\n")
    with open(filename2,'w') as backup:
        backup.write(backup_config + "\n\n")

if __name__=="__main__":

    fortinetBackup()