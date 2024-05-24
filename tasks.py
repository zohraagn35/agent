import subprocess
import platform
import re
import time

def is_firewall_active():
    if platform.system() == "Windows":
        def get_firewall_status():
            output = subprocess.run(["powershell", "-Command", "Get-NetFirewallProfile"], capture_output=True, text=True, shell=True).stdout
            pattern = re.compile(r'Name\s+:\s+(\w+)\s+Enabled\s+:\s+(\w+)', re.MULTILINE)
            matches = pattern.findall(output)
            firewall_status = {match[0]: match[1].lower() == 'true' for match in matches}
            return firewall_status
        firewall_status = get_firewall_status()
        return all(firewall_status.values())
    else:
        return True

def is_os_up_to_date():
    if platform.system() == "Windows":
        try:
            hotfix_output = subprocess.run(["powershell", "-Command", "Get-HotFix"], capture_output=True, text=True, shell=True).stdout
            if "No updates are installed" in hotfix_output:
                return True
            security_updates_installed = any("Security Update" in line for line in hotfix_output.splitlines())
            updates_installed = any("Update" in line for line in hotfix_output.splitlines())
            return security_updates_installed and updates_installed
        except Exception as e:
            print(f"Error occurred while checking OS update status: {e}")
            return False
    else:
        return True

def run_virus_scan():
    if platform.system() == "Windows":
        try:
            subprocess.run(["powershell", "-Command", "Start-MpScan -ScanType QuickScan"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("Failed to run virus scan.")
            return False
    else:
        return True
       

def reset_8021x_adapter():
    if platform.system() == "Windows":
        try:
            disable_output = subprocess.run(["powershell", "-Command", "Disable-NetAdapter -Name '802.1x' -Confirm:$false"], capture_output=True, text=True, shell=True).stdout
            time.sleep(3)
            enable_output = subprocess.run(["powershell", "-Command", "Enable-NetAdapter -Name '802.1x' -Confirm:$false"], capture_output=True, text=True, shell=True).stdout
            return True
        except Exception as e:
            print(f"Error occurred while resetting the adapter: {e}")
            return False
    else:
        print("Linux platform")
        return False


  
def check_domain():
    if platform.system() == "Windows":
        try:
            domain_output = subprocess.run(["powershell", "-Command", "Get-WmiObject -Class Win32_ComputerSystem"], capture_output=True, text=True, shell=True).stdout
            if "sonatrach.com" in domain_output:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occurred while checking domain status: {e}")
            return False
    else:
        return True
