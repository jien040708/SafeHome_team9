import tkinter as tk
from tkinter import Label, Button, Text
from abc import ABC, abstractmethod


class DeviceControlPanelAbstract(tk.Toplevel, ABC):
    """
    None a new root must exist before creating a Toplevel; callers
    should create the global `tk.Tk()` first (the `main.py` runner does).
    """
    
    def __init__(self, master=None):
        # Initialize as a Toplevel window attached to `master`.
        tk.Toplevel.__init__(self, master=master)
        self.title("Control Panel")
        self.geometry("505x300")
        self.resizable(False, False)
        
        # Initialize message variables
        self.short_message1 = ""
        self.short_message2 = ""
        
        x_start = 15
        y_start = 15
        x_w1 = 100
        x_w2 = 40
        x_w3 = 80
        y_h1 = 90
        y_h2 = 70
        
        # Security Zone label
        # 눈에 더 잘보이도록 테두리 추가
        display_dummy = tk.Entry(self, justify='center', state='readonly',
                     bg='white', fg='black', font=('Arial', 10, 'bold'),
                     bd=2, relief='ridge')
        display_dummy.insert(0, "Security Zone")
        display_dummy.place(x=x_start, y=y_start, width=x_w1, height=y_h1)
        
        # Zone number display (larger font, more prominent)
        self.display_number = tk.Entry(self, justify='center', state='readonly',
                                       bg='yellow', fg='black', font=('Arial', 24, 'bold'))
        self.display_number.insert(0, "1")
        self.display_number.place(x=x_start + x_w1, y=y_start, width=x_w2, height=y_h1)
        
        # Status displays frame
        status_frame = tk.Frame(self, bg='white')
        status_frame.place(x=x_start + x_w1 + x_w2, y=y_start, width=x_w3, height=y_h1)
        
        self.display_away = tk.Entry(status_frame, justify='center', state='readonly',
                                     bg='white', fg='light gray')
        self.display_away.insert(0, "away")
        self.display_away.pack(fill='both', expand=True)
        
        self.display_stay = tk.Entry(status_frame, justify='center', state='readonly',
                                     bg='white', fg='light gray')
        self.display_stay.insert(0, "stay")
        self.display_stay.pack(fill='both', expand=True)
        
        self.display_not_ready = tk.Entry(status_frame, justify='center', state='readonly',
                                          bg='white', fg='light gray')
        self.display_not_ready.insert(0, "not ready")
        self.display_not_ready.pack(fill='both', expand=True)
        
        # Text display area
        self.display_text = Text(self, height=4, width=27, bg='white', fg='black',
                state='disabled', wrap='word', bd=2, relief='sunken')
        self.display_text.place(x=x_start, y=y_start,
                   width=x_w1 + x_w2 + x_w3 + 60, height=y_h1 + y_h2)
        self._update_display_text()
        
        # Button panel with grid layout
        button_frame = tk.Frame(self)
        button_frame.place(x=300, y=6, width=240, height=300)
        
        # Create button grid (9 rows x 5 columns)
        # Row 0: Labels
        tk.Label(button_frame, text="     on").grid(row=0, column=0)
        tk.Label(button_frame, text="").grid(row=0, column=1)
        tk.Label(button_frame, text="    off").grid(row=0, column=2)
        tk.Label(button_frame, text="").grid(row=0, column=3)
        tk.Label(button_frame, text="  reset").grid(row=0, column=4)
        
        # Row 1: 1, 2, 3
        Button(button_frame, text="1", bg='white', fg='black', 
               command=self.button1, width=3).grid(row=1, column=0)
        tk.Label(button_frame, text="").grid(row=1, column=1)
        Button(button_frame, text="2", bg='white', fg='black',
               command=self.button2, width=3).grid(row=1, column=2)
        tk.Label(button_frame, text="").grid(row=1, column=3)
        Button(button_frame, text="3", bg='white', fg='black',
               command=self.button3, width=3).grid(row=1, column=4)
        
        # Row 2: Empty
        for i in range(5):
            tk.Label(button_frame, text="").grid(row=2, column=i)
        
        # Row 3: 4, 5, 6
        Button(button_frame, text="4", bg='white', fg='black',
               command=self.button4, width=3).grid(row=3, column=0)
        tk.Label(button_frame, text="").grid(row=3, column=1)
        Button(button_frame, text="5", bg='white', fg='black',
               command=self.button5, width=3).grid(row=3, column=2)
        tk.Label(button_frame, text="").grid(row=3, column=3)
        Button(button_frame, text="6", bg='white', fg='black',
               command=self.button6, width=3).grid(row=3, column=4)
        
        # Row 4: Away, Stay, Code labels
        tk.Label(button_frame, text="  away").grid(row=4, column=0)
        tk.Label(button_frame, text="").grid(row=4, column=1)
        tk.Label(button_frame, text="   stay").grid(row=4, column=2)
        tk.Label(button_frame, text="").grid(row=4, column=3)
        tk.Label(button_frame, text="  code").grid(row=4, column=4)
        
        # Row 5: 7, 8, 9
        Button(button_frame, text="7", bg='white', fg='black',
               command=self.button7, width=3).grid(row=5, column=0)
        tk.Label(button_frame, text="").grid(row=5, column=1)
        Button(button_frame, text="8", bg='white', fg='black',
               command=self.button8, width=3).grid(row=5, column=2)
        tk.Label(button_frame, text="").grid(row=5, column=3)
        Button(button_frame, text="9", bg='white', fg='black',
               command=self.button9, width=3).grid(row=5, column=4)
        
        # Row 6: Empty
        for i in range(5):
            tk.Label(button_frame, text="").grid(row=6, column=i)
        
        # Row 7: *, 0, #
        Button(button_frame, text="*", bg='white', fg='black',
               command=self.button_star, width=3).grid(row=7, column=0)
        tk.Label(button_frame, text="").grid(row=7, column=1)
        Button(button_frame, text="0", bg='white', fg='black',
               command=self.button0, width=3).grid(row=7, column=2)
        tk.Label(button_frame, text="").grid(row=7, column=3)
        Button(button_frame, text="#", bg='white', fg='black',
               command=self.button_sharp, width=3).grid(row=7, column=4)
        
        # Row 8: Panic labels
        tk.Label(button_frame, text="(panic)").grid(row=8, column=0)
        tk.Label(button_frame, text="").grid(row=8, column=1)
        tk.Label(button_frame, text="").grid(row=8, column=2)
        tk.Label(button_frame, text="").grid(row=8, column=3)
        tk.Label(button_frame, text="(panic)").grid(row=8, column=4)
        
        # LED panel
        # LED 패널을 왼쪽으로 더 당겨 표시 (Security Zone 아래쪽으로 정렬)
        led_frame = tk.Frame(self)
        led_frame.place(x=30, y=y_start + y_h1 + y_h2, width=230, height=70)
        
        tk.Label(led_frame, text="armed").grid(row=0, column=0)
        tk.Label(led_frame, text="").grid(row=0, column=1)
        tk.Label(led_frame, text="power").grid(row=0, column=2)
        
        # Use Labels for LEDs — Buttons in disabled state on some platforms
        # ignore background changes, so Labels provide reliable color updates.
        self.led_armed = tk.Label(led_frame, bg='light gray', width=8, height=1, bd=2, relief='groove')
        self.led_armed.grid(row=1, column=0)

        tk.Label(led_frame, text="").grid(row=1, column=1)

        self.led_power = tk.Label(led_frame, bg='light gray', width=8, height=1, bd=2, relief='groove')
        self.led_power.grid(row=1, column=2)
    
    def _update_display_text(self):
        """Update the display text area with current messages."""
        self.display_text.config(state='normal')
        self.display_text.delete('1.0', tk.END)
        text = f"\n{self.short_message1}\n{self.short_message2}"
        self.display_text.insert('1.0', text)
        self.display_text.config(state='disabled')
    

    def set_security_zone_number(self, num):
        """Set the security zone number display."""
        self.display_number.config(state='normal')
        self.display_number.delete(0, tk.END)
        self.display_number.insert(0, str(num))
        self.display_number.config(state='readonly')
    
    def set_display_away(self, on):
        """Set the 'away' display state."""
        self.display_away.config(fg='black' if on else 'light gray')
    
    def set_display_stay(self, on):
        """Set the 'stay' display state."""
        self.display_stay.config(fg='black' if on else 'light gray')
    
    def set_display_not_ready(self, on):
        """Set the 'not ready' display state."""
        self.display_not_ready.config(fg='black' if on else 'light gray')
    
    def set_display_short_message1(self, message):
        """Set the first short message line."""
        self.short_message1 = message
        self._update_display_text()
    
    def set_display_short_message2(self, message):
        """Set the second short message line."""
        self.short_message2 = message
        self._update_display_text()
    
    def set_armed_led(self, on):
        """Set the armed LED state."""
        self.led_armed.config(bg='red' if on else 'light gray')
    
    def set_powered_led(self, on):
        """Set the power LED state."""
        self.led_power.config(bg='green' if on else 'light gray')
    
    # Abstract button methods - must be implemented by subclasses
    @abstractmethod
    def button1(self):
        """Handle button 1 press."""
        pass
    
    @abstractmethod
    def button2(self):
        """Handle button 2 press."""
        pass
    
    @abstractmethod
    def button3(self):
        """Handle button 3 press."""
        pass
    
    @abstractmethod
    def button4(self):
        """Handle button 4 press."""
        pass
    
    @abstractmethod
    def button5(self):
        """Handle button 5 press."""
        pass
    
    @abstractmethod
    def button6(self):
        """Handle button 6 press."""
        pass
    
    @abstractmethod
    def button7(self):
        """Handle button 7 press."""
        pass
    
    @abstractmethod
    def button8(self):
        """Handle button 8 press."""
        pass
    
    @abstractmethod
    def button9(self):
        """Handle button 9 press."""
        pass
    
    @abstractmethod
    def button_star(self):
        """Handle * button press."""
        pass
    
    @abstractmethod
    def button0(self):
        """Handle button 0 press."""
        pass
    
    @abstractmethod
    def button_sharp(self):
        """Handle # button press."""
        pass

