#!/usr/bin/env python3
import os
import random
import time
import subprocess
import sys
import signal

# Expanded Vendor MAC prefixes
VENDOR_PREFIXES = {
    1: ('Apple', ['00:16:cb', '00:17:f2', '00:1e:c2']),
    2: ('Intel', ['00:02:b3', '00:1b:21', '00:21:6a']),
    3: ('Samsung', ['00:1d:25', '00:12:fb', '00:0d:bf']),
    4: ('Cisco', ['00:1b:54', '00:24:14', '00:40:96']),
    5: ('Dell', ['00:14:22', '00:1a:a0', '00:1b:fc']),
    6: ('Sony', ['00:13:a9', '00:13:15', '00:13:46']),
    7: ('Huawei', ['00:1a:8d', '00:15:2d', '00:18:82']),
    8: ('Lenovo', ['00:23:68', '00:26:c7', '00:50:b6']),
    9: ('Asus', ['00:1a:92', '00:1b:fc', '00:22:15']),
    10: ('Random', None)  # Option for completely random MAC addresses
}

original_mac = None  # Global variable to store the original MAC address

# Function to display the ASCII logo
def logo():
    print(r"""
 __  __          _____ _____           _           
|  \/  |   /\   / ____/ ____|         | |          
| \  / |  /  \ | |   | |    _   _  ___| | ___ _ __ 
| |\/| | / /\ \| |   | |   | | | |/ __| |/ _ \ '__|
| |  | |/ ____ \ |___| |___| |_| | (__| |  __/ |   
|_|  |_/_/    \_\_____\_____\__, |\___|_|\___|_|   
                             __/ |                 
                            |___/                  
|--------------------------------------------------------------------|
| Created By: Krishna Gopal Jha                                      |
| Checkout my LinkedIn: https://www.linkedin.com/in/krishnagopaljha/ |
| Lookup at my insta: https://instagram.com/theindianpsych           |
|--------------------------------------------------------------------| 
    """)

def get_current_mac(interface):
    """Get the current MAC address of the given interface."""
    result = subprocess.run(['ifconfig', interface], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'ether' in line:
            return line.strip().split()[1]
    return None

def random_mac(vendor=None):
    """Generate a random MAC address, optionally for a specific vendor."""
    if vendor and vendor != 'Random':
        mac_prefix = random.choice(vendor)
    else:
        mac_prefix = ':'.join(['%02x' % random.randint(0x00, 0xff) for _ in range(3)])
    
    mac_suffix = ':'.join(['%02x' % random.randint(0x00, 0xff) for _ in range(3)])
    return mac_prefix + ':' + mac_suffix

def set_mac(interface, mac_address):
    """Change the MAC address using macchanger."""
    subprocess.run(['ifconfig', interface, 'down'])
    subprocess.run(['macchanger', '-m', mac_address, interface])
    subprocess.run(['ifconfig', interface, 'up'])

def generate_and_set_mac(interface, vendor=None):
    """Generate and set a new MAC address."""
    new_mac = random_mac(vendor)
    set_mac(interface, new_mac)
    print(f"New MAC: {new_mac} for {interface}")

def restore_original_mac(interface):
    """Restore the original MAC address."""
    global original_mac
    if original_mac:
        print(f"Restoring original MAC: {original_mac}")
        set_mac(interface, original_mac)

def handle_exit_signal(signal_received, frame):
    """Handle the termination signals like CTRL+C."""
    print("\nTermination signal received. Restoring original MAC address.")
    restore_original_mac(interface)
    sys.exit(0)

def change_mac_periodically(interface, interval, vendor=None):
    """Change MAC address periodically with optional vendor spoofing."""
    while True:
        generate_and_set_mac(interface, vendor)
        time.sleep(interval)

def select_vendor():
    """Provide vendor options to the user and return the corresponding vendor prefix list."""
    print("Choose a vendor for MAC address spoofing:")
    for option, (vendor_name, _) in VENDOR_PREFIXES.items():
        print(f"{option}. {vendor_name}")
    
    try:
        choice = int(input("Enter the number corresponding to your choice: "))
        if choice in VENDOR_PREFIXES:
            return VENDOR_PREFIXES[choice][1]  # Return the vendor's MAC prefix list or None for random
        else:
            print("Invalid choice, using random MAC generation.")
            return None
    except ValueError:
        print("Invalid input, using random MAC generation.")
        return None

def validate_configuration(interface, interval):
    """Validate the configuration and check for correctness."""
    if subprocess.run(['ifconfig', interface], capture_output=True).returncode != 0:
        print("Invalid network interface.")
        sys.exit(1)
    
    if not isinstance(interval, int):
        print("Time interval should be an integer.")
        sys.exit(1)

def main():
    global original_mac
    # Display the ASCII logo
    logo()

    # Prompt user for input
    interface = input("Enter network interface (e.g., eth0): ")
    interval = int(input("Enter time interval in seconds (e.g., 60 for 1 minutes): "))
    vendor = select_vendor()

    # Validate the configuration
    validate_configuration(interface, interval)

    # Get and store the original MAC address
    original_mac = get_current_mac(interface)
    if not original_mac:
        print(f"Could not retrieve the MAC address for {interface}.")
        sys.exit(1)

    print(f"Original MAC address: {original_mac}")
    print(f"Starting MAC changer on {interface} with {interval} seconds interval.")

    # Set up signal handler for graceful termination (CTRL+C)
    signal.signal(signal.SIGINT, handle_exit_signal)

    # Start the periodic MAC address changer
    change_mac_periodically(interface, interval, vendor)

if __name__ == "__main__":
    main()
