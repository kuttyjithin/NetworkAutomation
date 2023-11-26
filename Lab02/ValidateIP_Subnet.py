#Function to Validate the IP address
def validate_ip_Address(ip_address):
    try:
        
        #remove any extra characters from the IP Address
        ip_address=ip_address.strip()

        #initialize a flag to point to true for an ip address
        ip_address_flag=True

        #validate if there are only 3 dots (.) in ip address
        if (not(ip_address.count('.') == 3)):
            ip_address_flag=False
        else:
            #stores each octet as a string
            ip_addressoctets=ip_address.split(".")

            #checks if the first octet is not zero
            if (int(ip_addressoctets[0]) ==0):
                    ip_address_flag=False

            #Validate if each of the octet is in range 0 - 255
            for octet in ip_addressoctets:
                octet=int(octet)
                if (not(octet <=255 & octet >=0)):
                    ip_address_flag=False

        #based upon the flag value display the relevant message
        if (ip_address_flag):
            return True
        else:
            return False
    except:
        return False

#Function to validate the subnet Mask
def validate_subnet(subnet):
    try:
        
        #remove any extra characters from the IP Address
        subnet=subnet.strip()

        #initialize a flag to point to true for an ip address
        subnet_flag=True

        if len(subnet) <= 3:

            cidr=subnet[1:]
            cidr=int(cidr)
            if ( 8 <= cidr <=32):
                # print("Entered Valid Subnet")
                return True
         #validate if there are only 3 dots (.) in ip address
        if (not(subnet.count('.') == 3)):
            subnet_flag=False
        else:
            #Validate if each of the octet is in range 0 - 255
            subnet_addressoctets=subnet.split(".")
            valid_subnet=[0,128,192,224,240,248,252,254,255]

            #checks if the first octet is 255
            if (not(int(subnet_addressoctets[0]) == 255)):
                subnet_flag= False

            #checks of th efirst octer is greater than the other occtet
            if(not(int(subnet_addressoctets[0])>=int(subnet_addressoctets[1]) and int(subnet_addressoctets[1])>=int(subnet_addressoctets[2]))):
               subnet_flag=False
            if(not(int(subnet_addressoctets[2])>=int(subnet_addressoctets[3]))):
                subnet_flag = False
           
            #Check if the each octet is valid
            for octet in subnet_addressoctets:
                #this variable becomes 1 if it is in avalid sunbnet range
                check_octet=0
                for subnet in valid_subnet:
                    if (int(octet) == subnet):
                         
                         check_octet = 1
                #Checks if it is the right octet
                if check_octet != 1:
                    subnet_flag=False

    #Return true if subnet mask is right and false if wrong
        if(subnet_flag):
            return True
        else:
            return False
               
    except:
        return False

def main(ip_address, subnet):

   

     
    #Starting an Exception handling where it prints Invalid Errror if something goes inside the loop
    try:
        #count variable to exit the programme if user input invalid input for more than 5 times
        count = 0
         #ntialize the variable to store the steing variable 
        interface_dict={}
        final_ip_address_subnet_mask = []
        while True:

            #ask the user to inut the the ip address and check if it valid
            # ip_address = input("Enter IP address. Type Quit to exit this application:")
            

            #Checking whether the user has entered  Input quit
            if ip_address == "Quit" or ip_address == "quit":
                print("Appreciate your turn! Have a Wonderful Day")
                # print (final_ip_address_subnet_mask)
                break

            #Checking whether the IP addres entered by user is Valid using the Validate_ip address function 
            elif (validate_ip_Address(ip_address) == True) :
                print("Valid IP")
                # key = 'IP-Address'
                # #stores the key with the IP address 
                # interface_dict[key]=ip_address

            #check if the Valid is invalid and adds 1 to the count if it is an invalid entry   
            else:
                print ("Invalid Entry, Please Try Again!")
                count = count + 1
                if(count >=5):
                    print("You have Enterd an wrong Value for more than 5 times, Exciting the applicatiom")
                    # print(final_ip_address_subnet_mask)
                    break
                

            # subnet = input("Enter subnet mask. Type Quit to exit this application:")
            #Checking whether the user has entered  Input quit
            if subnet == "quit" or subnet == "Quit":
                print("Appreciate your turn! Have a Wonderful Day")
                print (final_ip_address_subnet_mask)
                break

            #Checking whether the IP addres entered by user is Valid using the validat_sunbnet function 
            elif ( validate_subnet(subnet) == True):
                print("valid Subnet")
                break
                #stores the varaiable into the key subnet
                # key = 'subnet'
                # interface_dict[key]=subnet
                # final_ip_address_subnet_mask.append(interface_dict.copy())
                # interface_dict={}
            #check if the Valid is invalid and adds 1 to the count if it is an invalid entry 
            else:
                print ("Invalid Entry, Please Try Again!")
                count = count + 1
                if(count >=5):
                    print("You have Enterd an wrong Value for more than 5 times, Exciting the applicatiom")
                    # print(final_ip_address_subnet_mask)
                    break

                
    except:
        print("an error has occurred")
    


if __name__=="__main__":

    main()

    