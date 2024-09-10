# MAC Changer Tool

This Python script is a powerful tool for periodically changing the MAC address of a network interface in Kali Linux. It allows users to spoof their MAC address to one from a specific vendor or generate a completely random one.

## Features

- **Periodic MAC Address Change**: Automatically changes the MAC address at a specified time interval.
- **Vendor Spoofing**: Allows users to select a MAC address prefix from major vendors such as Apple, Intel, Cisco, and others.
- **Random MAC Option**: Option to generate a completely random MAC address.
- **Real-time MAC Change**: Displays the newly generated MAC address after every change.

## Requirements

- Python 3.x
- `macchanger` utility (pre-installed on Kali Linux)
- Root privileges to change the MAC address

## Installation

1. Clone the repository or download the script:

    ```bash
    git clone https://github.com/krishnagopaljha/maccycler.git
    cd maccycler
    ```

2. Make sure you have Python 3 installed:

    ```bash
    sudo apt-get install python3
    ```

3. Ensure that `macchanger` is installed (usually pre-installed in Kali Linux):

    ```bash
    sudo apt-get install macchanger
    ```

## Usage

1. Run the script as root:

    ```bash
    sudo python3 mac_changer.py
    ```

2. When prompted, enter the network interface (e.g., `wlan0`, `eth0`), the time interval for periodic MAC changes (in seconds), and the vendor of your choice from the list provided. Alternatively, choose the random option for a completely random MAC address.

3. To stop the script and restore the original MAC address, press `CTRL+C`.

## Example

```bash
$ sudo python3 mac_changer.py
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

Enter network interface (e.g., wlan0): wlan0
Enter time interval in seconds (e.g., 600 for 10 minutes): 600
Choose a vendor for MAC address spoofing:
1. Apple
2. Intel
3. Samsung
...
10. Random
Enter the number corresponding to your choice: 1
Original MAC address: 00:1a:2b:3c:4d:5e
Starting MAC changer on wlan0 with 600 seconds interval.
New MAC: 00:16:cb:12:34:56 for wlan0
```

## How It Works

- The script prompts for a network interface, time interval, and vendor.
- Every X seconds (specified by the user), the MAC address is automatically changed to either a vendor-specific or random MAC address.
