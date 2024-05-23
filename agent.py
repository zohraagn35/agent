import subprocess
import tkinter as tk
from tkinter import ttk , messagebox
import time
import threading
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
        # Assume Linux does not have firewall check implemented
        return True

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
        # Assume Linux is always up to date for this dummy implementation
        return True

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
        # Assume Linux does not need a virus scan for this dummy implementation
        return True

# GUI functions
def create_gui():
    global root, status_var, continue_execution
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

  # Add check_domain function to the list of task_functions
    task_labels = ["Checking Firewall", "Checking Updates", "Running Virus Scan", "Checking Domain"]
    task_functions = [check_firewall, check_updates, run_scan, check_domain]


    continue_execution = True

    for i, (label_text, task) in enumerate(zip(task_labels, task_functions)):
        if continue_execution:
            label = tk.Label(root, text=label_text, bg="white", fg="black")
            label.pack(pady=10)
            canvas = tk.Canvas(root, width=50, height=50, bg="white", highlightthickness=0)
            canvas.pack(pady=10)
            task_info = (task, canvas, label)
            threading.Thread(target=run_task, args=(task_info, i)).start()
        else:
            break

    root.mainloop()

def run_task(task_info, index):
    global continue_execution
    task, canvas, label = task_info
    if continue_execution:
        animate_circle(canvas)
        task()
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="green", outline="green")
        label.config(text=label.cget("text") + " - Completed")
        update_status(index)
        root.update()
    else:
        messagebox.showwarning("Task Stopped", "Task has stopped. Please correct any issues to continue.")
        return

def animate_circle(canvas):
    for _ in range(20):  # Adjust the range for longer or shorter animation
        for angle in range(0, 360, 30):  # Adjust the step for smoother or rougher animation
            canvas.delete("all")
            x = 25 + 15 * math.cos(math.radians(angle))
            y = 25 + 15 * math.sin(math.radians(angle))
            canvas.create_oval(x-10, y-10, x+10, y+10, fill="yellow", outline="yellow")
            root.update()
            time.sleep(0.1)

def update_status(index):
    status_messages = [
        "Checking Firewall...",
        "Checking Updates...",
         "Running Virus Scan...",
        "All tasks completed!"
    ]
    status_var.set(status_messages[index + 1])
    root.update()

def check_firewall():
    global continue_execution
    time.sleep(2)  # Simulate task delay
    if platform.system() == "Windows":
        if is_firewall_active():
            status_var.set("Firewall is active.")
        else:
            status_var.set("Firewall is not active.")
            continue_execution = False
    else:
        status_var.set("Firewall check not applicable for Linux.")
        continue_execution = False
    root.update()

# Function to check if the user's Windows machine is in the domain "sonatrach.com"
def check_domain():
    global continue_execution
    if platform.system() == "Windows":
        try:
            domain_output = subprocess.run(["powershell", "-Command", "Get-WmiObject -Class Win32_ComputerSystem"], capture_output=True, text=True, shell=True).stdout
            if "sonatrach.com" in domain_output:
                status_var.set("Machine is in the 'sonatrach.com' domain.")
            else:
                status_var.set("Machine is not in the 'sonatrach.com' domain. Please log in to the 'sonatrach.com' domain to access the network.")
                continue_execution = False
        except Exception as e:
            print(f"Error occurred while checking domain status: {e}")
            status_var.set("Error occurred while checking domain status.")
            continue_execution = False
    else:
        status_var.set("Domain check not applicable for non-Windows systems.")
        continue_execution = False


def check_updates():
    global continue_execution
    time.sleep(2)  # Simulate task delay
    if platform.system() == "Windows":
        if is_os_up_to_date():
            status_var.set("OS is up to date.")
        else:
            status_var.set("OS update required.")
            continue_execution = False
    else:
        status_var.set("Update check not applicable for Linux.")
        continue_execution = False
    root.update()




def run_scan():
    global continue_execution
    time.sleep(2)  # Simulate task delay
    if platform.system() == "Windows":
        if continue_execution:
            run_virus_scan()
            status_var.set("Virus scan completed.")
        else:
            return
    else:
        continue_execution = False
        status_var.set("Virus scan not applicable for Linux.")
    root.update()

if __name__ == "__main__":
    create_gui()
