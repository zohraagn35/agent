import tkinter as tk
from tkinter import messagebox
import math
import time
from tasks import *
def create_gui():
    global root, status_var, bg_image
    root = tk.Tk()
    root.title("802.1X Agent")
    root.geometry("700x700")
    root.resizable(False, False)
    
    bg_image = tk.PhotoImage(file="agent2.png")
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)

    title_label = tk.Label(root, text="AGENT NAC", font=("Helvetica", 24, "bold"), bg="white")
    title_label.pack(pady=20)

    status_var = tk.StringVar()
    status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 12), bg="white", fg="black")
    status_label.pack(pady=20)

    task_labels = ["Checking Firewall", "Checking Updates", "Running Virus Scan", "Checking Domain"]
    task_functions = [check_firewall_task, check_updates_task, run_scan_task, check_domain_task]
    task_statuses = []

    for i, (label_text, task) in enumerate(zip(task_labels, task_functions)):
        label = tk.Label(root, text=label_text, bg="white", fg="black")
        label.pack(pady=10)
        canvas = tk.Canvas(root, width=50, height=50, bg="white", highlightthickness=0)
        canvas.pack(pady=10)
        animate_circle(canvas)
        success = task(canvas, label)
        task_statuses.append(success)

    if all(task_statuses):
        reset_8021x_adapter()

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
        return True
    else:
        update_status("Firewall is not active.")
        messagebox.showwarning("Task Stopped", "Firewall is not active. Please enable the firewall.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="red", outline="red")
        label.config(text=label.cget("text") + " - not Completed")
        return False

def check_updates_task(canvas, label):
    if is_os_up_to_date():
        update_status("OS is up to date.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="green", outline="green")
        label.config(text=label.cget("text") + " - Completed")
        return True
    else:
        update_status("OS update required.")
        messagebox.showwarning("Task Stopped", "OS update is required. Please update your OS.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="red", outline="red")
        label.config(text=label.cget("text") + " - not Completed")
        return False

def run_scan_task(canvas, label):
    if run_virus_scan():
        update_status("Virus scan completed.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="green", outline="green")
        label.config(text=label.cget("text") + " - Completed")
        return True
    else:
        update_status("Failed to complete virus scan.")
        messagebox.showwarning("Task Stopped", "Virus scan failed. Please check your antivirus software.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="red", outline="red")
        label.config(text=label.cget("text") + " - not Completed")
        return False

def check_domain_task(canvas, label):
    if check_domain():
        update_status("Machine is in the 'sonatrach.com' domain.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="green", outline="green")
        label.config(text=label.cget("text") + " - Completed")
        return True
    else:
        update_status("Machine is not in the 'sonatrach.com' domain.")
        messagebox.showwarning("Task Stopped", "Machine is not in the 'sonatrach.com' domain. Please log in to the 'sonatrach.com' domain to access the network.")
        canvas.delete("all")
        canvas.create_oval(10, 10, 40, 40, fill="red", outline="red")
        label.config(text=label.cget("text") + " - not Completed")
        return False
