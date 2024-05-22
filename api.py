import ctypes 
from ctypes import wintypes  

# load ddl eapol
try:
    eapproxy = ctypes.WinDLL('eappprxy.dll')
    print("Successfully loaded eappprxy.dll")
except OSError as e:
    print(f"Error loading eappprxy.dll: {e}")
