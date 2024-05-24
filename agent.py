import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import time
import platform
import re
import math

# Function to check if firewall is active on Windows
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
        return True  # Assume non-Windows systems are always okay

# Function to check if OS is up to date (dummy implementation)
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
        return False  # Assume non-Windows systems are always okay

# Function to run a virus scan (dummy implementation)
def run_virus_scan():
    if platform.system() == "Windows":
        try:
            subprocess.run(["powershell", "-Command", "Start-MpScan -ScanType QuickScan"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("Failed to run virus scan.")
            return False
    else:
        return False  # Assume non-Windows systems are always okay

# Function to check if the user's Windows machine is in the domain "sonatrach.com"
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
        return False  # Assume non-Windows systems are always okay

# GUI functions
def create_gui():
    global root, status_var, bg_image
    root = tk.Tk()
    root.title("802.1X Agent")
    root.geometry("700x700")
    root.resizable(False, False)
    
    bg_image = tk.PhotoImage(file="agent.png")
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)

    title_label = tk.Label(root, text="AGENT NAC", font=("Helvetica", 24, "bold"), bg="white")
    title_label.pack(pady=20)

    status_var = tk.StringVar()
    status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 12), bg="white", fg="black")
    status_label.pack(pady=20)

    task_labels = ["Checking Firewall", "Checking Updates", "Running Virus Scan", "Checking Domain"]
    task_functions = [check_firewall_task, check_updates_task, run_scan_task, check_domain_task]

    
    for i, (label_text, task) in enumerate(zip(task_labels, task_functions)): 
            label = tk.Label(root, text=label_text, bg="white", fg="black")
            label.pack(pady=10)
            canvas = tk.Canvas(root, width=50, height=50, bg="white", highlightthickness=0)
            canvas.pack(pady=10)
            animate_circle(canvas)
            success = task(canvas, label)  # Check if the task succeeded
           
                
                

    root.mainloop()

def animate_circle(canvas):
    for _ in range(5):
        for angle in range(0, 360, 15):
            canvas.delete("all")
            x = 25 + 15 * math.cos(math.radians(angle))
            y = 25 + 15 * math.sin(math.radians(angle))
            canvas.create_oval(x-10, y-10, x+10, y+10, fill="yellow", outline="yellow")
            root.update()
            time.sleep(0.03)

def update_status(message):
    status_var.set(message)
    root.update()

def check_firewall_task(canvas, label):
    if is_firewall_active():
        update_status("Firewall is active.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="green", outline="green")
        label.config(text=label.cget("text") + " - Completed")
    else:
        update_status("Firewall is not active.")
        messagebox.showwarning("Task Stopped", "Firewall is not active. Please enable the firewall.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="red", outline="red")
        label.config(text=label.cget("text") + " - not Completed")
    


def check_updates_task(canvas, label):
    if is_os_up_to_date():
        update_status("OS is up to date.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="green", outline="green")
        label.config(text=label.cget("text") + " - Completed")

    else:
        update_status("OS update required.")
        messagebox.showwarning("Task Stopped", "OS update is required. Please update your OS.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="red", outline="red")
        label.config(text=label.cget("text") + " - not Completed")


def run_scan_task(canvas, label):
    if run_virus_scan():
        update_status("Virus scan completed.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="green", outline="green")
        label.config(text=label.cget("text") + " - Completed")
    else:
        update_status("Failed to complete virus scan.")
        messagebox.showwarning("Task Stopped", "Virus scan failed. Please check your antivirus software.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="red", outline="red")
        label.config(text=label.cget("text") + " - not Completed")

def check_domain_task(canvas, label):
    if check_domain():
        update_status("Machine is in the 'sonatrach.com' domain.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="green", outline="green")
        label.config(text=label.cget("text") + " - Completed")
    else:
        update_status("Machine is not in the 'sonatrach.com' domain.")
        messagebox.showwarning("Task Stopped", "Machine is not in the 'sonatrach.com' domain. Please log in to the 'sonatrach.com' domain to access the network.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="red", outline="red")
        label.config(text=label.cget("text") + " - not Completed")

if __name__ == "__main__":
    create_gui()
