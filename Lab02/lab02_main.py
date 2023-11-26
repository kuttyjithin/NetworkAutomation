import json
import ValidateIP_Subnet
import Backup
import restore
import clearfortinet
import json_file


# Function to handle the user's choice for backup, restore, or clearing configurations
def choice():
    try:
        Prog_Name = """\t Student Assignment  Lab02 . Created by Jithin Jose, Saiban Muhammad, Walod M Rana .  Written on 10/31/2023
            *******************************************************************************************************************************
            NETW3100 Fall 2023
            This program Backup, Restore and Clear  the Configuration
            **********************************************************************************************************************************
            """
        print (Prog_Name)
        username = input("Enter the username: ")
        if username.lower() == 'quit':
            exit(1)
        password = input("Enter the password: ")
        if username.lower() == 'quit':
            exit(1)


        while True:
            ipaddress_mask = input("Enter the Network address and Mask: ")
            
            # Determine if the user entered IP and mask in the format "x.x.x.x/y" or "x.x.x.x y"
            if "/" in ipaddress_mask:
                ipaddress_mask= ipaddress_mask.split("/")
                ipaddress=ipaddress_mask[0]
                mask="/"+ipaddress_mask[1]
                if (ValidateIP_Subnet.validate_ip_Address(ipaddress) and ValidateIP_Subnet.validate_subnet(mask)):
                    print("Valid")
                    break
                else:
                    print("not Valid")

            elif " " in ipaddress_mask:
                ipaddress_mask= ipaddress_mask.split(" ")
                ipaddress=ipaddress_mask[0]
                mask=ipaddress_mask[1]
                if (ValidateIP_Subnet.validate_ip_Address(ipaddress) and ValidateIP_Subnet.validate_subnet(mask)):
                    print("Valid")
                    break
                else:
                    print("not Valid")
                
            else:
                mask = input("Enter the subnet Mask: ")
                ipaddress = ipaddress_mask
                if (ValidateIP_Subnet.validate_ip_Address(ipaddress) and ValidateIP_Subnet.validate_subnet(mask)):
                    print("Valid")
                    break
                else:
                    print("not Valid")

        

        # Perform initial device scanning and JSON file creation
        json_file.scan(ipaddress,username,password)

        Group_Name = """\t\t*******************************************************************************************************************************
                A. Backup the running configuration of each network device and store it in a text file named after device’s hostname with a date-time stamp
                B. Restore Configurations from an Existing Backup to devices’ running configuration files.
                C.  Clear configs on the FortiGate"
                ********************************************************************************************************************************************
            """
        print (Group_Name)

        count = 0
        while True:
            
            

            #Validate the user input according to A/B/C
            user_input = input("Enter A/B/C: ")
            if user_input.lower() == "a":
                Backup.backup(ipaddress,username,password)
            elif user_input.lower() == 'b':
                restore.restore(ipaddress,username,password)
            elif user_input.lower() == 'c':
                clearfortinet.clear_config()
            elif user_input.lower() == 'quit':
                break
            else:
                print ("Invalid Entry, Please Try Again!")
                count = count + 1
                if(count >=5):
                    print("You have Enterd an wrong Value for more than 5 times, Exciting the applicatiom")
                    # print(final_ip_address_subnet_mask)
                    break


    except:
        print("an eror has occured")

#error exception for loop
if __name__=="__main__":

    choice()
