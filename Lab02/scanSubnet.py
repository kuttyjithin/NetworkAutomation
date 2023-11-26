
from ping3 import ping



def scan(subnet):
    try:
        #Splits the devce into four octet
        ip_addressoctets=subnet.split(".")
        device_list = []

        #Loop to scan first 17 ip address in the range
        for i in range(1,18):
            ip_to_scan= f"{ip_addressoctets[0]}.{ip_addressoctets[1]}.{ip_addressoctets[2]}.{i}"
            response_time = ping(ip_to_scan, timeout=1)

            #Check if the response time is none and if it is none it adds as a list
            if response_time != None:
                device_list.append(ip_to_scan)
            
            
           
        #Prints the devices Online   
        print( "Device Online:")
        print( device_list)
        return device_list
        
    except:
        print("error")

if __name__=="__main__":

    scan("192.168.3.0")