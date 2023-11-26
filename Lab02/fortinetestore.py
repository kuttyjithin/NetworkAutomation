#Libarary required to run this python file
from netmiko import ConnectHandler
from ping3 import ping


#Function to restore the Fortinet Switch
def fortinetRestore():
    try:
        cisco_881 = {
                'device_type': 'fortinet',
                'host':   '192.168.3.18',
                'username': 'admin',
                'password': 'P@ssw0rd',
                }
        net_connect = ConnectHandler(**cisco_881)
        
        #Function to get the hostname 
        hostname = net_connect.send_command('get system status').split('Hostname: ')[1].split('\n')[0]
        restore_file="backups\\"+hostname+".txt"
        print(restore_file)

        #Opens the files and restore the comands line by line to the networking devices
        with open(restore_file, 'r') as file_lines:
            command= file_lines.read().splitlines()
            print("**********************************\n")
            print("REstoring " + hostname)
            print("\n**********************************")

            #Inputs the command on the netwrking devices. 
            input = net_connect.send_config_set(command,cmd_verify=False)
            print(input)
    except:
        print("Error")


    
    
if __name__=="__main__":

    fortinetRestore()