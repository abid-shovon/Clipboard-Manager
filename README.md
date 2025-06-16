# Clipboard Manager

## Overview

This Clipboard Manager application captures and stores your clipboard history including **text and images**, and displays them in a user-friendly GUI.  
You can quickly open the clipboard history window by pressing **Alt + V**.

---

## Supported Platforms

- **Linux** (tested mainly on Ubuntu with GNOME desktop)  
- **Windows** (should work with PyQt5 and pynput, but global hotkeys and autostart are better supported on Linux)

---

## Features

- Capture and store up to 100 clipboard items (text and images)  
- Display clipboard history in a GUI using PyQt5  
- Open the Clipboard Manager window via a global hotkey: **Alt + V**  
- Double-click any history item to copy it back to the clipboard  
- Automatically avoid duplicate entries in history  
- System tray icon for quick access and quitting the app  
- Easy to configure for autostart on Linux at system boot

---

## Requirements

- Python 3.6 or higher  
- PyQt5  
- pynput


## Installation and Running

1. Clone or download the project:
  
`git clone <https://github.com/abid-shovon/Clipboard-Manager.git> cd clipboard_manager` 

2.  Install dependencies:

`pip install pyqt5 pynput` 

3.  Run the program:


`python3 main.py` 

----------

## Running in Background

To run the program in the background (so it keeps running after you close the terminal):


`nohup python3 /full/path/to/main.py > ~/clipboard_manager.log 2>&1 &` 

----------

## Autostart on Linux (Ubuntu GNOME)

To have the clipboard manager start automatically when you log in:

1.  Create the autostart directory if it does not exist:


`mkdir -p ~/.config/autostart` 

2.  Create a new file:


`nano ~/.config/autostart/clipboard_manager.desktop` 

3.  Paste the following into the file, updating the `Exec` path to your full main.py location:
    

`[Desktop Entry]  

Type=Application 

Exec=python3 /home/hasan/Desktop/projects_of_python/clipboard_manager/main.py 

Hidden=false  

NoDisplay=false  

X-GNOME-Autostart-enabled=true 

Name=Clipboard Manager 

Comment=Start Clipboard Manager at login` 


4.  Save and close the file (`Ctrl+O`, Enter, then `Ctrl+X`).
    
    
5.  Make it executable (optional):

`chmod +x 
~/.config/autostart/clipboard_manager.desktop` 

6.  Restart your computer. The program will launch automatically.
    

----------

## Notes

-   The global hotkey **Alt + V** works as long as the program is running in the background.
    
-   Closing VS Code or the terminal does not stop the program if it was started as a background process or via autostart.
    
-   To quit the program, use the "Quit" option from the system tray icon menu.
