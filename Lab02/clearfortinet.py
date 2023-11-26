
#Liabray required for the function 
from netmiko import ConnectHandler

#This function clear the config on this device.
def clear_config():

    # Define device parameters
    device = {
        'device_type': 'fortinet',
        'ip':   "192.168.3.18",
        'username': 'admin',
        'password':'P@ssw0rd',
    }

    # Establish an SSH connection to the device
    connection = ConnectHandler(**device)

    

    # Send commands to the device and print the output
    print("""\t\t*************************************************
            Resetting device to factory defaults...
          *************************************************\n""")
    connection.config_mode()
    connection.send_command_timing('execute factoryreset', strip_prompt=False, strip_command=False)
    connection.send_command_timing('y', strip_prompt=False, strip_command=False)
    print("""\t\t*************************************************
                        Fortinet Resetted
          *************************************************\n""")


if __name__=="__main__":

    clear_config()



