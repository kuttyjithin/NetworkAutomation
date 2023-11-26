import config # connects, configs router and tests connectivity 
import GenerateReport # connects and gets info and then generate report

# call the file on a different folder as nornir is located on a different folder 
import sys
sys.path.append('C:\\Users\\Jithin Jose\\OneDrive - NAIT\\BAITS\\NETW3100\\NETW3100\\nornir_lab03')
#calls the nornir
import start 

#calls the modules main function
def main():
    
    print("\n----------------------Config Network Devices---------------------\n")
    config.main()
    print("\n----------------------Config Network Devices---------------------\n")


    print("\n----------------------Generating Report ---------------------\n")
    GenerateReport.info()
    print("\n----------------------Generating Report ---------------------\n")

    print("\n----------------------Sequential Library(Netmiko) vs Concurrency Library(Nornir)  ---------------------\n")
    start.main()
    print("\n----------------------Sequential Library(Netmiko) vs Concurrency Library(Nornir)  ---------------------\n")

#run main() if main file
if __name__=="__main__":

    main()