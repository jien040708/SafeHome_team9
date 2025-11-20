import tkinter as tk
from tkinter import ttk

PAGES = ("Login", "MainMenu", "Zones", "Modes", "Monitoring")


class SafeHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SafeHome Prototype")
        self.configure(bg="#d9d9d9")
        self.geometry("640x480")
        self.resizable(False, False)

        self.style = ttk.Style(self)
        self.style.configure("TFrame", background="#d9d9d9")
        self.style.configure("Section.TLabel", font=("Helvetica", 16, "bold"), background="#d9d9d9")
        self.style.configure("Title.TLabel", font=("Helvetica", 28, "bold"), background="#d9d9d9")
        self.style.configure("Primary.TButton", font=("Helvetica", 12), padding=(20, 8))

        container = ttk.Frame(self)
        container.pack(expand=True, fill="both")

        self.frames = {}
        for page in PAGES:
            cls = globals()[f"{page}View"]
            frame = cls(parent=container, controller=self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("Login")

    def show_page(self, name: str):
        self.frames[name].tkraise()


class LoginView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="SafeHome", style="Title.TLabel").pack(pady=(40, 30))
        panel = ttk.Frame(self, padding=30, relief="groove")
        panel.pack()
        ttk.Label(panel, text="LOGIN SAFEHOME SYSTEM", font=("Helvetica", 12, "bold")).pack(pady=(0, 20))
        self.user_entry = ttk.Entry(panel, width=30)
        self.pass_entry = ttk.Entry(panel, width=30, show="•")
        ttk.Label(panel, text="User ID").pack(anchor="w")
        self.user_entry.pack(pady=(0, 10))
        ttk.Label(panel, text="Password").pack(anchor="w")
        self.pass_entry.pack(pady=(0, 20))
        ttk.Button(panel, text="LOGIN", style="Primary.TButton",
                   command=lambda: controller.show_page("MainMenu")).pack()


class MainMenuView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="SafeHome", style="Title.TLabel").pack(pady=(40, 30))
        for target, label in [("Zones", "SECURITY"), ("Modes", "SURVEILLANCE"), ("Monitoring", "CONFIGURE")]:
            ttk.Button(self, text=label, style="Primary.TButton",
                       command=lambda t=target: controller.show_page(t)).pack(pady=10, ipadx=30)


class ZonesView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: controller.show_page("MainMenu")).pack(side="right")

        nav = ttk.Frame(self)
        nav.pack(side="left", fill="y", padx=10, pady=10)
        for label in ["Add Safety zone", "Update Safety zone", "Delete Safety zone"]:
            ttk.Button(nav, text=label, style="Primary.TButton").pack(pady=5, fill="x")

        ttk.Label(nav, text="Safety zone status", font=("Helvetica", 12, "bold")).pack(pady=(20, 5))
        for zone in ["Zone A — Activated", "Zone B — Deactivated", "Zone C — Deactivated", "Zone D — Activated"]:
            ttk.Label(nav, text=zone).pack(anchor="w")

        canvas = tk.Canvas(self, width=420, height=320, bg="white", highlightthickness=2, highlightbackground="black")
        canvas.pack(side="left", padx=20, pady=20)
        canvas.create_text(210, 20, text="SAFETY ZONE MONITORING", font=("Helvetica", 12, "bold"))
        canvas.create_rectangle(40, 60, 380, 280, dash=(4, 2))
        canvas.create_text(210, 305, text="First Floor", font=("Helvetica", 10, "italic"))


class ModesView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: controller.show_page("MainMenu")).pack(side="right")

        nav = ttk.Frame(self)
        nav.pack(side="left", fill="y", padx=10, pady=10)
        for label in ["Home", "Away", "Overnight Travel", "Extended Travel", "Guest Home", "Arm/Disarm all sensors"]:
            ttk.Button(nav, text=label, style="Primary.TButton").pack(pady=5, fill="x")

        canvas = tk.Canvas(self, width=420, height=320, bg="white", highlightthickness=2, highlightbackground="black")
        canvas.pack(side="left", padx=20, pady=20)
        canvas.create_text(210, 20, text="SECURITY MODE MONITORING", font=("Helvetica", 12, "bold"))
        canvas.create_rectangle(40, 60, 380, 280, dash=(4, 2))
        canvas.create_text(210, 305, text="First Floor", font=("Helvetica", 10, "italic"))


class MonitoringView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: controller.show_page("MainMenu")).pack(side="right")

        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=10)
        for label in ["Access", "Configure", "System Status", "View", "Monitoring"]:
            ttk.Button(toolbar, text=label).pack(side="left", padx=5)

        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 10))
        ttk.Label(left, text="RECORDING").pack(anchor="w")
        for label in ["BEGIN", "STOP", "SHOW"]:
            ttk.Button(left, text=label, style="Primary.TButton").pack(fill="x", pady=3)
        ttk.Label(left, text="PASSWORD", padding=(0, 10, 0, 0)).pack(anchor="w")
        for label in ["SET", "DELETE"]:
            ttk.Button(left, text=label).pack(fill="x", pady=3)

        control = ttk.Frame(main)
        control.pack(side="left", fill="both", expand=True)
        ttk.Button(control, text="ENABLE/DISABLE").pack(side="left", padx=5)
        ttk.Button(control, text="VIEW").pack(side="left", padx=5)

        monitor_area = ttk.Frame(main)
        monitor_area.pack(fill="both", expand=True, pady=10)
        canvas = tk.Canvas(monitor_area, width=260, height=200, bg="white", highlightthickness=2, highlightbackground="black")
        canvas.grid(row=0, column=0, padx=10)
        canvas.create_text(130, 20, text="Monitoring", font=("Helvetica", 12, "bold"))

        cam_status = ttk.Frame(monitor_area, padding=10, relief="ridge")
        cam_status.grid(row=0, column=1, padx=10, sticky="n")
        ttk.Label(cam_status, text="CAMERA STATUS", font=("Helvetica", 12, "bold")).pack()
        for row in ["ID ........ CAMERA1", "RUNNING ... ON", "RECORDING . ON", "LOCK ....... OFF"]:
            ttk.Label(cam_status, text=row).pack(anchor="w")

        video = tk.Canvas(monitor_area, width=260, height=120, bg="white", highlightthickness=2, highlightbackground="black")
        video.grid(row=1, column=1, padx=10, pady=10)
        video.create_text(130, 15, text="Video Image — LR", font=("Helvetica", 10, "italic"))

        sliders = ttk.Frame(monitor_area)
        sliders.grid(row=1, column=0, pady=10)
        ttk.Label(sliders, text="Zoom").pack(anchor="w")
        tk.Scale(sliders, from_=0, to=10, orient="horizontal").pack()
        ttk.Label(sliders, text="Pan").pack(anchor="w")
        tk.Scale(sliders, from_=0, to=10, orient="horizontal").pack()


if __name__ == "__main__":
    SafeHomeApp().mainloop()