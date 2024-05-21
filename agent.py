import subprocess 
import tkinter as tk
from tkinter import messagebox
from scapy.all import *
from scapy.layers.eap import EAP
# from radius_eap_mschapv2 import RADIUS

# """ |||||||||||| |||||| |||||| ||||||  |||||| """
# radius_host = '192.168.30.5'
# radius_secret = 'Zola123:'
# radius_nas_ip = '192.168.30.10'
# radius_nas_id = 'mynas'
# username = 'myuser'
# password = 'adel'
# """ |||||||||||| |||||| |||||| |||||| |||||| ||||||"""




# Function to check if firewall is active on Windows
def is_firewall_active():
    """Checks if the Windows Firewall is active.

    Returns:
        bool: True if the firewall is active, False otherwise.
    """
    # Function to get the firewall status
    def get_firewall_status():
        # Run the command using PowerShell (requires shell=True)
        output = subprocess.run(["powershell", "-Command", "Get-NetFirewallProfile"], capture_output=True, text=True, shell=True).stdout

        # Regular expression pattern to extract firewall status
        pattern = re.compile(r'Name\s+:\s+(\w+)\s+Enabled\s+:\s+(\w+)', re.MULTILINE)

        # Find all matches in the output
        matches = pattern.findall(output)

        # Dictionary to store firewall status
        firewall_status = {}

        # Iterate through matches and populate the dictionary
        for match in matches:
            profile = match[0]
            enabled = True if match[1].lower() == 'true' else False
            firewall_status[profile] = enabled

        return firewall_status

    # Get the firewall status
    firewall_status = get_firewall_status()

    # Check if any profile has the firewall disabled
    for profile, enabled in firewall_status.items():
        if not enabled:
            return False
    
    return True

# Function to check if OS is up to date (dummy implementation)
def is_os_up_to_date():
    """Checks if the Windows operating system is up to date.

    Returns:
        bool: True if the OS is up to date, False otherwise.
    """
    try:
        # Run the PowerShell command to get installed hotfixes
        hotfix_output = subprocess.run(["powershell", "-Command", "Get-HotFix"], capture_output=True, text=True, shell=True).stdout

        # Check if there are any installed hotfixes
        if "No updates are installed" in hotfix_output:
            return True  # No updates installed means the system is up to date
        else:
            # Check if any security updates are installed
            security_updates_installed = any("Security Update" in line for line in hotfix_output.splitlines())

            # Check if any updates are installed
            updates_installed = any("Update" in line for line in hotfix_output.splitlines())

            # If both security updates and general updates are installed, consider the system up to date
            if security_updates_installed and updates_installed:
                return True
            else:
                return False

    except Exception as e:
        print(f"Error occurred while checking OS update status: {e}")
        return False


# Function to run a virus scan (dummy implementation)
def run_virus_scan():
    """Runs a virus scan using Windows Defender (Windows PowerShell).

    Returns:
        bool: True if the scan was initiated successfully, False otherwise.
    """
    try:
        # Run the PowerShell command to start a quick scan
        subprocess.run(["powershell", "-Command", "Start-MpScan -ScanType QuickScan"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Failed to run virus scan.")
        return False


# Function to send packet to the switch using scapy
def login_8021x():
         
    # r = RADIUS(radius_host, radius_secret, radius_nas_ip, radius_nas_id)
    # print(r.is_credential_valid(username, password))
# Create GUI
def create_gui():
    # Create main window
    root = tk.Tk()
    root.title("802.1X Agent")
    # root.size = (500,500)

    # Create buttons for each action
    firewall_button = tk.Button(root, text="Check Firewall", command=check_firewall, bg="red", fg="black")
    firewall_button.pack(pady=20)

    update_button = tk.Button(root, text="Check Updates", command=check_updates, bg="lightgreen", fg="black")
    update_button.pack(pady=20)

    virus_scan_button = tk.Button(root, text="Run Virus Scan", command=run_scan, bg="orange", fg="black")
    virus_scan_button.pack(pady=20)

    login_button = tk.Button(root, text="Login 802.1X", command=login_8021x, bg="lightblue", fg="black")
    login_button.pack(pady=20)


    # Run GUI loop
    root.mainloop()

# Functions to be called when buttons are clicked
def check_firewall():
    if is_firewall_active():
        messagebox.showinfo("Firewall Status", "Firewall is active.")
    else:
        messagebox.showinfo("Firewall Status", "Firewall is not active.")

def check_updates():
    if is_os_up_to_date():
        messagebox.showinfo("Update Status", "OS is up to date.")
    else:
        messagebox.showinfo("Update Status", "OS update required.")

def run_scan():
    run_virus_scan()
    messagebox.showinfo("Virus Scan", "Virus scan completed.")


# Start GUI
if __name__ == "__main__":
    create_gui()
