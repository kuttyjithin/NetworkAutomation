from netmiko import ConnectHandler
import json
import napalm
import time
def scan():
    # subnet =subnet.strip()
    # ip_addressoctets=subnet.split(".")

    # for i in range(1,256):
    #     ip_to_scan= f"{ip_addressoctets[0]}.{ip_addressoctets[1]}.{ip_addressoctets[2]}.{i}"
    #     print(ip_to_scan)
    #     cisco_881 = {
    #     'device_type': 'cisco_ios',
    #     'host':   ip_to_scan,
    #     'username': 'cisco',
    #     'password': 'cisco',
    #     }
    cisco_881 = {
        'device_type': 'cisco_ios',
        'host':   '192.168.3.17',
        'username': 'cisco',
        'password': 'cisco',
        }
    

    
    

    net_connect = ConnectHandler(**cisco_881)
    # output = net_connect.send_command('show ip int br' , use_textfsm=True)
    output = net_connect.send_command('show run') 
    # python_json=json.loads(output)
    # print (python_json)
    print(output)
    
    hostname = net_connect.send_command('show run | include hostname')
    hostname=hostname.strip().split("hostname ")[-1]
    restore_file="backups\\"+hostname+".txt"
    print(restore_file)

    with open(restore_file, 'r') as file_lines:
        command= file_lines.read().splitlines()
            
    print("**********************************\n")
    print("Restoring " + hostname)
    print("\n**********************************")
    
    for com in command:
        input = net_connect.send_config_set(com,cmd_verify=False)
    
    print(input)

    # with open("routerconfig.txt","w")as configFie:
    #     configFie.write(output)


def main():

    scan()

if __name__ == "__main__":
    main()