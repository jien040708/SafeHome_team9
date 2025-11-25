#!/usr/bin/env python3
"""
Control Panel Example
=====================
This example demonstrates the SafeHome Control Panel GUI with:
- Number keypad (0-9, *, #)
- LED indicators (armed, power)
- Status displays (away, stay, not ready)
- Message display area

Usage:
    python -m example.example_control_panel
    OR
    python example_control_panel.py (when run from example directory)
"""

import sys
import tkinter as tk
from pathlib import Path

# Add parent directory to path for direct script execution
if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

# Try relative import first (for package execution), fall back to absolute
try:
    from device.device_control_panel_abstract import DeviceControlPanelAbstract
except ImportError:
    from ..device.device_control_panel_abstract import DeviceControlPanelAbstract

# Example implementation for testing
class TestControlPanel(DeviceControlPanelAbstract):
    """Concrete implementation for testing the control panel."""
    
    def __init__(self):
        super().__init__()
        self.set_display_short_message1("System Ready")
        self.set_display_short_message2("Enter Code")
        self.set_powered_led(True)
        self.button_sequence = ""
    
    def button1(self):
        print("Button 1 pressed")
        self.button_sequence += "1"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
    
    def button2(self):
        print("Button 2 pressed")
        self.button_sequence += "2"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
    
    def button3(self):
        print("Button 3 pressed")
        self.button_sequence += "3"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
        # Simulate arming after 1-2-3
        if self.button_sequence == "123":
            self.set_armed_led(True)
            self.set_display_away(True)
            self.set_display_short_message1("System Armed")
    
    def button4(self):
        print("Button 4 pressed")
        self.button_sequence += "4"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
    
    def button5(self):
        print("Button 5 pressed")
        self.button_sequence += "5"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
    
    def button6(self):
        print("Button 6 pressed")
        self.button_sequence += "6"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
    
    def button7(self):
        print("Button 7 pressed")
        self.button_sequence += "7"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
    
    def button8(self):
        print("Button 8 pressed")
        self.button_sequence += "8"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
    
    def button9(self):
        print("Button 9 pressed")
        self.button_sequence += "9"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
    
    def button_star(self):
        print("Button * pressed (Panic)")
        self.set_armed_led(True)
        self.set_display_short_message1("PANIC ALARM!")
        self.set_display_short_message2("Help on the way")
    
    def button0(self):
        print("Button 0 pressed")
        self.button_sequence += "0"
        self.set_display_short_message2(f"Code: {self.button_sequence}")
        self.set_display_not_ready(True)
        self.set_security_zone_number(4)
    
    def button_sharp(self):
        print("Button # pressed (Reset/Panic)")
        # Reset sequence
        self.button_sequence = ""
        self.set_armed_led(False)
        self.set_display_away(False)
        self.set_display_stay(False)
        self.set_display_not_ready(False)
        self.set_display_short_message1("System Ready")
        self.set_display_short_message2("Enter Code")


if __name__ == "__main__":
    # Create root window and hide it
    root = tk.Tk()
    root.withdraw()
    
    # Run the test control panel
    app = TestControlPanel()
    print("Control Panel GUI started")
    print("Try entering code 1-2-3 to arm the system")
    print("Press * for panic alarm")
    print("Press # to reset")
    app.mainloop()
