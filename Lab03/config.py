import json  # Import JSON module for handling JSON data
from netmiko import ConnectHandler  # Import ConnectHandler from Netmiko for SSH connections

# Function to apply global configurations to network devices
def apply_global_config(net_connect, device_config):
    try:
        print(f"Entering Global Configuration Mode for {device_config['hostname']}")
        if device_config['device_type'] == "cisco_ios":
            # Define configuration commands for global settings
            config_commands = [
                f"hostname {device_config['hostname']}",
                "no logging console"
            ]

            # Check if the device is a switch and has a gateway configuration
            if 'gateway' in device_config:
                config_commands.append(device_config['gateway'])

            # Send global configuration commands to the device
            input = net_connect.send_config_set(config_commands)
            print(input)

            # Retrieve and display the current hostname
            hostname = net_connect.send_command('show run | include hostname')
            hostname = hostname.strip().split("hostname ")[-1]
            print(f"Current hostname: {hostname}")

    except Exception as e:
        print(f"Failed to apply global config to {device_config['hostname']}: {str(e)}")


# Function to apply interface configurations to network devices
def apply_interface_config(net_connect, device_config):
    try:
        print(f"Configuring Interfaces for {device_config['hostname']}")
        if device_config['device_type'] == "cisco_ios":
            # Iterate through interfaces and their configurations
            for interface, config in device_config.get('interfaces', {}).items():
                if config:
                    # Define configuration commands for each interface
                    config_commands = [
                        f"interface {interface}",
                        f"ip address {config.get('ip address', '').strip()}",  # Remove extra spaces
                        f"{config.get('ospf', '')}",
                        f"{config.get('shut', '')}"
                    ]
                    # Apply interface configuration commands to the device
                    net_connect.send_config_set(config_commands)
                    print(f"Interface {interface} configured for {device_config['hostname']}")

    except Exception as e:
        print(f"Failed to apply interface config to {device_config['hostname']}: {str(e)}")

# Function to apply routing configurations to network devices
def apply_routing_config(net_connect, device_config):
    try:
        print(f"Configuring Routing for {device_config['hostname']}")
        if device_config['device_type'] == "cisco_ios":
            # Retrieve routing configurations
            router_config = device_config.get('router-config', {})
            if router_config:
                # Define routing configuration commands
                config_commands = [
                    router_config.get('protocol', ''),
                    f"router-id {router_config.get('router-id', '')}",
                    router_config.get('network1', ''),
                    router_config.get('network2', '')
                ]
                # Apply routing configuration commands to the device
                net_connect.send_config_set(config_commands)
                print(f"Routing configured for {device_config['hostname']}")

    except Exception as e:
        print(f"Failed to apply routing config to {device_config['hostname']}: {str(e)}")

# Function to ping interfaces of network devices
def ping_interfaces(devices):
    failed_pings = []

    try:
        # Iterate through source devices
        for source_device in devices:
            for source_device_name, source_device_config in source_device.items():
                print(f"Pinging interfaces from {source_device_config['hostname']}")

                # Connect to the source device using Netmiko
                source_net_connect = ConnectHandler(
                    device_type=source_device_config['device_type'],
                    host=source_device_config['host'],
                    username=source_device_config['username'],
                    password=source_device_config['password']
                )

                # Iterate through target devices
                for target_device in devices:
                    for target_device_name, target_device_config in target_device.items():
                        if source_device_name != target_device_name:
                            # Iterate through interfaces and their configurations in the target device
                            for interface, config in target_device_config.get('interfaces', {}).items():
                                if config and 'ip address' in config:
                                    ip_address = config['ip address'].split()[0]  # Extract the IP address

                                    # Construct and execute ping command
                                    print(f"Pinging {ip_address} from {source_device_config['hostname']} to {target_device_config['hostname']}")
                                    try:
                                        # Perform ping from source to target interface
                                        result = source_net_connect.send_command(f'ping {ip_address}', delay_factor=3)

                                        # Display ping results
                                        print(f"Ping result from {source_device_config['hostname']} to {target_device_config['hostname']} - {interface} ({ip_address}):")
                                        print(result)
                                        if "Unreachable" in result or "100% packet loss" in result:
                                            print("Error: Ping unsuccessful")
                                            failed_pings.append(
                                                f"Failed ping from {source_device_config['hostname']} to {target_device_config['hostname']} - {interface} ({ip_address})"
                                            )
                                    except Exception as e:
                                        print(f"Failed to ping interfaces: {str(e)}")

                # Disconnect from the source device
                source_net_connect.disconnect()

        # Print the list of failed pings, if any
        if failed_pings:
            print("\nFailed Pings:")
            for failed_ping in failed_pings:
                print(failed_ping)
        else:
            print("\nAll pings successful.")

    except Exception as e:
        print(f"Failed to ping interfaces: {str(e)}")

# Main function to execute the entire configuration process
def main():
    try:
        # Open and read devices' configurations from a JSON file
        with open('devices.json', 'r') as json_file:
            devices = json.load(json_file)

        # Iterate through devices and their configurations
        for device in devices:
            for device_name, device_config in device.items():
                try:
                    # Connect to the device using Netmiko
                    net_connect = ConnectHandler(
                        device_type=device_config['device_type'],
                        host=device_config['host'],
                        username=device_config['username'],
                        password=device_config['password']
                    )

                    # Apply global, interface, and routing configurations to the device
                    apply_global_config(net_connect, device_config)
                    apply_interface_config(net_connect, device_config)
                    apply_routing_config(net_connect, device_config)

                    # Disconnect from the device
                    net_connect.disconnect()

                except Exception as e:
                    print(f"An error occurred while configuring {device_config['hostname']}: {str(e)}")

        # Ping interfaces of all devices at the end
        ping_interfaces(devices)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Execute the main function when the script is run
if __name__ == "__main__":
    main()
