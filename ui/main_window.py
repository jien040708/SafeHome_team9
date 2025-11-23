import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional

from PIL import Image, ImageTk
import os
from utils.constants import *
from security.interfaces import SecurityEventListener

# 페이지 이름 상수
PAGES = ("Login", "MainMenu", "Zones", "Modes", "Monitoring")


class TkSecurityListener(SecurityEventListener):
    """Adapter that routes SecuritySystem events to the Tkinter UI."""

    def __init__(self, app: "SafeHomeApp"):
        self.app = app

    def _run_on_ui(self, callback, *args, **kwargs):
        if not getattr(self.app, "root", None):
            return
        self.app.root.after(0, lambda: callback(*args, **kwargs))

    def on_status_changed(self, status):
        text = f"{status.mode.name} ({status.alarm_state.name})"
        self._run_on_ui(self.app.update_status_label, text, status.armed_zones)

    def on_intrusion_logged(self, record):
        sensor = record.sensor_id or "Unknown sensor"
        zone = record.zone_id or "Zone ->"
        timestamp = record.timestamp.strftime("%H:%M:%S")
        message = f"[{timestamp}] {record.action} at {sensor} ({zone})"
        self._run_on_ui(self.app.add_log, message)
        self._run_on_ui(self.app.add_intrusion_log, message)

    def on_entry_delay_started(self, event, deadline):
        deadline_str = deadline.strftime("%H:%M:%S")
        msg = f"Entry delay started for {event.sensor_id or 'Unknown'} (until {deadline_str})"
        self._run_on_ui(self.app.add_log, msg)

    def on_alarm_activated(self, event):
        sensor = event.sensor_id if event else "Unknown"
        alert_msg = f"ALARM! Triggered by {sensor}"
        self._run_on_ui(self.app.show_alert, alert_msg)
        self._run_on_ui(self.app.add_log, f"Alarm activated ({sensor})")

    def on_alarm_cleared(self, cleared_by: str):
        message = f"Alarm cleared by {cleared_by}"
        self._run_on_ui(self.app.add_log, message)

class SafeHomeApp:
    def __init__(self, root, system, sensors):
        self.root = root
        self.system = system  # System 인스턴스
        self.controller = system.system_controller  # 기존 호환성 유지
        self.sensors = sensors
        
        self.root.title("SafeHome Prototype")
        self.root.configure(bg="#d9d9d9")
        self.root.geometry("800x600") # 이미지 표시를 위해 크기 조정
        self.root.resizable(False, False)

        # 스타일 설정 (기존 코드 스타일 유지)
        self.style = ttk.Style(self.root)
        self.style.configure("TFrame", background="#d9d9d9")
        self.style.configure("Section.TLabel", font=("Helvetica", 16, "bold"), background="#d9d9d9")
        self.style.configure("Title.TLabel", font=("Helvetica", 28, "bold"), background="#d9d9d9")
        self.style.configure("Primary.TButton", font=("Helvetica", 12), padding=(20, 8))

        container = ttk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.images = {}  # ->-> -> ->->
        self.intrusion_logs: list[str] = []

        # -> ->-> ->
        for page_name in PAGES:
            cls = globals()[f"{page_name}View"]
            frame = cls(parent=container, system=self.system, sensors=self.sensors, app=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # -> ->-> ->
        self.create_status_bar()

        # -> ->
        self.show_page("Login")
        self._security_tick()

    def create_status_bar(self):
        bar = tk.Frame(self.root, bg="black", height=30)
        bar.pack(side="bottom", fill="x")
        self.status_label = tk.Label(bar, text="System Ready", fg="white", bg="black", font=("Arial", 10))
        self.status_label.pack(side="left", padx=10)

    def show_page(self, name):
        frame = self.frames[name]
        frame.tkraise()
        # 페이지 전환 시 상태 갱신 (ModesView 등에서 최신 상태 반영 위해)
        if hasattr(frame, 'refresh'):
            frame.refresh()

    def update_status_label(self, text, armed_zones=None):
        self.status_label.config(text=f"Status: {text}")
        # Modes ->-> ->-> -> ->
        if "Modes" in self.frames:
            self.frames["Modes"].update_mode_display(text, armed_zones)

    def add_log(self, message):
        current = self.status_label.cget("text")
        if len(current) > 80: current = current[:80] + "..."
        self.status_label.config(text=f"{current} | {message}")

    def add_intrusion_log(self, message: str):
        """Store intrusion log entries and refresh Monitoring view."""
        self.intrusion_logs.append(message)
        if len(self.intrusion_logs) > 1000:
            self.intrusion_logs = self.intrusion_logs[-1000:]

        monitoring = self.frames.get("Monitoring")
        if monitoring and hasattr(monitoring, "update_intrusion_log"):
            monitoring.update_intrusion_log(self.intrusion_logs)

    def show_alert(self, msg):
        messagebox.showwarning("ALARM", msg)

    def load_image(self, path, size):
        """이미지 로드 헬퍼 함수 (에러 처리 포함)"""
        try:
            if not os.path.exists(path):
                return None
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            return photo
        except Exception as e:
            print(f"Image load error: {e}")
            return None

    def _security_tick(self):
        """Periodically advance the SecuritySystem, allowing entry delays to expire."""
        try:
            if self.system and getattr(self.system, "security_system", None):
                self.system.security_system.tick(datetime.utcnow())
        except Exception as exc:
            print(f"[UI] Security tick error: {exc}")
        finally:
            if getattr(self, "root", None):
                self.root.after(1000, self._security_tick)


# --- View Classes (기존 UI 디자인 반영) ---

class LoginView(ttk.Frame):
    def __init__(self, parent, system, sensors, app):
        super().__init__(parent)
        self.system = system
        self.app = app
        self.is_locked = False

        ttk.Label(self, text="SafeHome", style="Title.TLabel").pack(pady=(40, 30))

        self.panel = ttk.Frame(self, padding=30, relief="groove")
        self.panel.pack()

        ttk.Label(self.panel, text="LOGIN SAFEHOME SYSTEM", font=("Helvetica", 12, "bold")).pack(pady=(0, 20))

        # Status message label (for showing remaining attempts, etc.)
        self.status_label = ttk.Label(self.panel, text="", font=("Helvetica", 10), foreground="blue")
        self.status_label.pack(pady=(0, 10))

        self.user_entry = ttk.Entry(self.panel, width=30)
        self.pass_entry = ttk.Entry(self.panel, width=30, show="•")

        ttk.Label(self.panel, text="User ID").pack(anchor="w")
        self.user_entry.pack(pady=(0, 10))

        ttk.Label(self.panel, text="Password").pack(anchor="w")
        self.pass_entry.pack(pady=(0, 20))

        self.login_btn = ttk.Button(self.panel, text="LOGIN", style="Primary.TButton",
                   command=self.attempt_login)
        self.login_btn.pack()

        # Bind Enter key to login
        self.user_entry.bind('<Return>', lambda e: self.attempt_login())
        self.pass_entry.bind('<Return>', lambda e: self.attempt_login())

    def attempt_login(self):
        uid = self.user_entry.get()
        pw = self.pass_entry.get()

        if not uid or not pw:
            messagebox.showwarning("Input Required", "Please enter both User ID and Password")
            return

        # Common Function 1: Log onto the system through control panel
        result = self.system.login_with_details(uid, pw, interface='control_panel')

        if result['success']:
            # Login successful - unlock UI if it was locked
            if self.is_locked:
                self.unlock_control_panel()

            self.status_label.config(text="", foreground="blue")
            self.app.show_page("MainMenu")
        else:
            # Login failed
            if result.get('locked'):
                # Account locked - show remaining time
                remaining_time = result.get('remaining_time', 0)

                if remaining_time > 0:
                    # 시간 기반 잠금 - 남은 시간 표시
                    minutes = remaining_time // 60
                    seconds = remaining_time % 60
                    time_msg = f"{minutes} minutes {seconds} seconds" if minutes > 0 else f"{seconds} seconds"

                    self.status_label.config(
                        text=f"Account locked. Try again in {time_msg}",
                        foreground="red"
                    )
                    messagebox.showerror("Account Locked",
                                       f"{result.get('message', 'Account is locked.')}\n\n"
                                       f"Please try again in {time_msg}.")
                else:
                    # 잠금 직후 또는 시간 정보 없음 - 메시지만 표시 (UI는 잠그지 않음)
                    self.status_label.config(
                        text=f"Account locked. Please wait and try again.",
                        foreground="red"
                    )
                    messagebox.showerror("Account Locked",
                                       f"{result.get('message', 'Account is locked.')}\n\n"
                                       "Please wait a moment and try again.")
            elif result.get('system_locked'):
                # System locked
                messagebox.showerror("System Locked", result.get('message', 'System is locked.'))
            elif result.get('system_off'):
                # System off
                messagebox.showerror("System Off", result.get('message', 'System is off.'))
            else:
                # Incorrect password - show remaining attempts
                tries = result.get('tries', 0)
                remaining = result.get('remaining', 0)

                if remaining > 0:
                    self.status_label.config(
                        text=f"Login failed. Remaining attempts: {remaining}",
                        foreground="red"
                    )
                    messagebox.showerror("Login Failed",
                                       f"Incorrect password.\n\n"
                                       f"Failed attempts: {tries}\n"
                                       f"Remaining attempts: {remaining}")
                else:
                    self.status_label.config(text="", foreground="blue")
                    messagebox.showerror("Login Failed", result.get('message', 'Login failed'))

            # Clear password field
            self.pass_entry.delete(0, tk.END)
            self.pass_entry.focus()

    def lock_control_panel(self):
        """Lock the control panel UI"""
        self.is_locked = True

        # Disable input fields
        self.user_entry.config(state='disabled')
        self.pass_entry.config(state='disabled')
        self.login_btn.config(state='disabled')

        # Show lock message
        self.status_label.config(
            text="🔒 CONTROL PANEL LOCKED",
            foreground="red",
            font=("Helvetica", 12, "bold")
        )

        print("[LoginView] Control panel locked due to too many failed attempts.")

    def unlock_control_panel(self):
        """Unlock the control panel UI (for admin use)"""
        self.is_locked = False

        # Enable input fields
        self.user_entry.config(state='normal')
        self.pass_entry.config(state='normal')
        self.login_btn.config(state='normal')

        # Clear lock message
        self.status_label.config(text="", foreground="blue", font=("Helvetica", 10))

        # Clear input fields
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

        print("[LoginView] Control panel unlocked.")


class MainMenuView(ttk.Frame):
    def __init__(self, parent, system, sensors, app):
        super().__init__(parent)
        self.system = system
        self.app = app

        ttk.Label(self, text="SafeHome", style="Title.TLabel").pack(pady=(40, 30))

        # 메뉴 버튼들
        for target, label in [("Zones", "SECURITY"), ("Modes", "SURVEILLANCE"), ("Monitoring", "CONFIGURE")]:
            ttk.Button(self, text=label, style="Primary.TButton",
                       command=lambda t=target: self.app.show_page(t)).pack(pady=10, ipadx=30)

        ttk.Button(self, text="LOGOUT",
                   command=self.logout).pack(pady=20)

    def logout(self):
        self.system.logout()
        self.app.show_page("Login")


class ZonesView(ttk.Frame):
    def __init__(self, parent, system, sensors, app):
        super().__init__(parent)
        self.system = system
        self.config_manager = system.configuration_manager
        self.controller = system.system_controller
        self.app = app
        self.sensors = sensors
        self.sensor_status_labels: dict[str, ttk.Label] = {}
        self.sensor_zone_labels: dict[str, ttk.Label] = {}
        self.zone_name_var = tk.StringVar()
        self.sensor_var = tk.StringVar()
        self.zone_assign_var = tk.StringVar()

        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: self.app.show_page("MainMenu")).pack(side="right")

        # Left navigation
        nav = ttk.Frame(self)
        nav.pack(side="left", fill="y", padx=10, pady=10)

        zone_frame = ttk.LabelFrame(nav, text="Safety Zones")
        zone_frame.pack(fill="x", pady=(0, 10))

        self.zone_list = tk.Listbox(zone_frame, height=8)
        self.zone_list.pack(fill="x", padx=5, pady=5)

        ttk.Label(zone_frame, text="Zone Name").pack(anchor="w", padx=5)
        ttk.Entry(zone_frame, textvariable=self.zone_name_var).pack(fill="x", padx=5, pady=(0, 5))
        ttk.Button(zone_frame, text="Add Zone", command=self.add_zone).pack(fill="x", padx=5, pady=2)
        ttk.Button(zone_frame, text="Rename Selected", command=self.rename_zone).pack(fill="x", padx=5, pady=2)
        ttk.Button(zone_frame, text="Delete Selected", command=self.delete_zone).pack(fill="x", padx=5, pady=(2, 5))

        assign_frame = ttk.LabelFrame(nav, text="Sensor Assignments")
        assign_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(assign_frame, text="Sensor").pack(anchor="w", padx=5)
        self.sensor_combo = ttk.Combobox(assign_frame, textvariable=self.sensor_var, state="readonly")
        self.sensor_combo.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Label(assign_frame, text="Zone").pack(anchor="w", padx=5)
        self.zone_combo = ttk.Combobox(assign_frame, textvariable=self.zone_assign_var, state="readonly")
        self.zone_combo.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Button(assign_frame, text="Assign Sensor to Zone", command=self.assign_sensor).pack(fill="x", padx=5, pady=2)
        ttk.Button(assign_frame, text="Clear Assignment", command=self.clear_sensor_assignment).pack(fill="x", padx=5, pady=(0, 5))
        self.assignment_feedback = ttk.Label(assign_frame, text="", foreground="green")
        self.assignment_feedback.pack(fill="x", padx=5, pady=(0, 5))

        ttk.Label(nav, text="Sensor Simulation", font=("Helvetica", 12, "bold")).pack(pady=(10, 5))

        for sensor in self.sensors:
            row = ttk.Frame(nav)
            row.pack(fill="x", pady=2)
            ttk.Label(row, text=sensor.get_id(), width=14).pack(side="left")
            status_text = self._get_initial_status(sensor)
            status_label = ttk.Label(row, text=status_text, width=10)
            status_label.pack(side="left", padx=(5, 10))
            self.sensor_status_labels[sensor.get_id()] = status_label

            zone_label = ttk.Label(row, text="Zone: -", width=12, foreground="gray40")
            zone_label.pack(side="left")
            self.sensor_zone_labels[sensor.get_id()] = zone_label

            ttk.Button(row, text="Trigger", width=8, command=lambda s=sensor: self.trigger_sensor(s)).pack(side="right")

        # Floorplan
        canvas_frame = tk.Frame(self, bg="white", highlightthickness=2, highlightbackground="black")
        canvas_frame.pack(side="left", padx=20, pady=20, expand=True)

        self.floor_img = self.app.load_image("floorplan.png", (400, 300))
        if self.floor_img:
            lbl_img = tk.Label(canvas_frame, image=self.floor_img, bg="white")
            lbl_img.image = self.floor_img
            lbl_img.pack()
        else:
            tk.Label(canvas_frame, text="[Floorplan Image Missing]", bg="white").pack(pady=50)

        tk.Label(canvas_frame, text="First Floor Layout", font=("Helvetica", 10, "italic"), bg="white").pack(pady=5)

        self.refresh_zone_list()
        self.refresh_sensor_assignments()

    def refresh(self):
        self.refresh_zone_list()
        self.refresh_sensor_assignments()

    def refresh_zone_list(self):
        zones = self.config_manager.refresh_safety_zones()
        self.zone_list.delete(0, tk.END)
        zone_display = []
        for zone in zones:
            display = f"[{zone.zone_id}] {zone.zone_name}"
            self.zone_list.insert(tk.END, display)
            zone_display.append(f"{zone.zone_id} - {zone.zone_name}")
        self.zone_combo['values'] = zone_display
        if zone_display and not self.zone_assign_var.get():
            self.zone_combo.current(0)

        devices = self.config_manager.device_manager.load_all_devices()
        sensor_ids = [device_id for device_id, _ in devices]
        if sensor_ids and not self.sensor_var.get():
            self.sensor_combo['values'] = sensor_ids
            self.sensor_combo.current(0)
        else:
            self.sensor_combo['values'] = sensor_ids

    def refresh_sensor_assignments(self):
        assignments = self.config_manager.list_sensor_assignments()
        zone_map = self.config_manager.get_zone_name_map()

        for sensor_id, label in self.sensor_zone_labels.items():
            zone_id = assignments.get(sensor_id)
            if zone_id is None:
                label.config(text="Zone: -", foreground="gray40")
            else:
                zone_name = zone_map.get(str(zone_id), str(zone_id))
                label.config(text=f"Zone: {zone_name}", foreground="steelblue")

    def _selected_zone_id(self) -> Optional[int]:
        if not self.zone_list.curselection():
            return None
        raw = self.zone_list.get(self.zone_list.curselection())
        try:
            zone_id = int(raw.split(']')[0].strip('['))
            return zone_id
        except Exception:
            return None

    def add_zone(self):
        name = self.zone_name_var.get().strip()
        if not name:
            messagebox.showerror("Input Required", "Enter a zone name.")
            return
        if self.config_manager.add_safety_zone(name):
            self.zone_name_var.set("")
            self.refresh_zone_list()

    def rename_zone(self):
        zone_id = self._selected_zone_id()
        if zone_id is None:
            messagebox.showerror("Select Zone", "Select a zone to rename.")
            return
        name = self.zone_name_var.get().strip()
        if not name:
            messagebox.showerror("Input Required", "Enter a new zone name.")
            return
        self.config_manager.modify_safety_zone(zone_id, zone_name=name)
        self.zone_name_var.set("")
        self.refresh_zone_list()

    def delete_zone(self):
        zone_id = self._selected_zone_id()
        if zone_id is None:
            messagebox.showerror("Select Zone", "Select a zone to delete.")
            return
        if messagebox.askyesno("Confirm", "Delete selected zone->"):
            self.config_manager.delete_safety_zone(zone_id)
            self.refresh_zone_list()
            self.refresh_sensor_assignments()

    def assign_sensor(self):
        sensor_id = self.sensor_var.get()
        zone_value = self.zone_assign_var.get()
        if not sensor_id or not zone_value:
            messagebox.showerror("Input Required", "Select both sensor and zone.")
            return
        try:
            zone_id = int(zone_value.split('-')[0].strip())
        except Exception:
            messagebox.showerror("Invalid Zone", "Unable to parse the selected zone.")
            return
        if self.config_manager.assign_sensor_to_zone(sensor_id, zone_id):
            self.assignment_feedback.config(text=f"{sensor_id} -> Zone {zone_id}", foreground="green")
            self.refresh_sensor_assignments()
        else:
            self.assignment_feedback.config(text="Assignment failed", foreground="red")

    def clear_sensor_assignment(self):
        sensor_id = self.sensor_var.get()
        if not sensor_id:
            messagebox.showerror("Input Required", "Select a sensor to clear.")
            return
        if self.config_manager.remove_sensor_assignment(sensor_id):
            self.assignment_feedback.config(text=f"{sensor_id} unassigned", foreground="orange")
            self.refresh_sensor_assignments()
        else:
            self.assignment_feedback.config(text="No assignment to clear", foreground="red")

    def trigger_sensor(self, sensor):
        sensor_type = sensor.get_type()
        status_for_controller = "Triggered"

        current_status = None
        if hasattr(sensor, "get_status"):
            try:
                current_status = sensor.get_status()
            except Exception:
                current_status = None

        if "Window" in sensor_type or "Door" in sensor_type:
            if current_status == STATE_CLOSED and hasattr(sensor, "set_open"):
                sensor.set_open()
                status_for_controller = "Open"
            else:
                if hasattr(sensor, "set_closed"):
                    sensor.set_closed()
                status_for_controller = "Closed"
        elif "Motion" in sensor_type:
            if hasattr(sensor, "detect_motion"):
                sensor.detect_motion()
            status_for_controller = "Motion Detected"
        else:
            if hasattr(sensor, "trigger"):
                sensor.trigger()

        label = self.sensor_status_labels.get(sensor.get_id())
        if label:
            label.config(text=self._status_label_text(sensor))

        if self.controller:
            try:
                self.controller.update_sensor_status(sensor.get_id(), sensor_type, status_for_controller)
            except Exception as exc:
                print(f"[ZonesView] Failed to forward sensor update: {exc}")

        self.app.add_log(f"{sensor.get_id()} {status_for_controller}")
        messagebox.showinfo("Sensor", f"{sensor.get_id()} {status_for_controller}!")

    def _get_initial_status(self, sensor):
        if hasattr(sensor, "get_status"):
            try:
                status = sensor.get_status()
                return "Closed" if status == STATE_CLOSED else status or "Unknown"
            except Exception:
                return "Unknown"
        return "Unknown"

    def _status_label_text(self, sensor):
        if hasattr(sensor, "get_status"):
            try:
                status = sensor.get_status()
                if status == STATE_CLOSED:
                    return "Closed"
                if status == STATE_OPEN:
                    return "Open"
                if status == STATE_DETECTED:
                    return "Motion"
                return status or "Unknown"
            except Exception:
                return "Unknown"
        return "Unknown"


class ModesView(ttk.Frame):
    def __init__(self, parent, system, sensors, app):
        super().__init__(parent)
        self.system = system
        self.controller = system.system_controller
        self.app = app

        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: self.app.show_page("MainMenu")).pack(side="right")

        nav = ttk.Frame(self)
        nav.pack(side="left", fill="y", padx=10, pady=10)

        modes = [("Arm Away", MODE_AWAY), ("Arm Stay", MODE_STAY), ("Disarm", MODE_DISARMED)]
        for label, mode_const in modes:
            ttk.Button(nav, text=label, style="Primary.TButton",
                       command=lambda m=mode_const: self.change_mode(m)).pack(pady=5, fill="x")
        for label in ["Overnight Travel", "Guest Home"]:
            ttk.Button(nav, text=label, style="Primary.TButton").pack(pady=5, fill="x")

        self.mode_display = ttk.Label(nav, text="Current: Disarmed (IDLE)", font=("Helvetica", 14, "bold"),
                                      foreground="blue")
        self.mode_display.pack(pady=(10, 0))
        self.zones_label = ttk.Label(nav, text="Armed Zones: All", font=("Helvetica", 11), foreground="gray25")
        self.zones_label.pack(pady=(0, 20))

        indicator_frame = ttk.Frame(nav)
        indicator_frame.pack(pady=(0, 15))
        ttk.Label(indicator_frame, text="Zone Indicator", font=("Helvetica", 10, "bold")).pack()
        self.zone_indicator = tk.Canvas(indicator_frame, width=20, height=20, highlightthickness=0, bg="#d9d9d9")
        self.zone_indicator.pack()
        self.zone_indicator_id = self.zone_indicator.create_oval(2, 2, 18, 18, fill="#a0aec0", outline="")
        self.zone_indicator_text = ttk.Label(indicator_frame, text="No zones armed", foreground="gray40")
        self.zone_indicator_text.pack()

        canvas_frame = tk.Frame(self, bg="white", highlightthickness=2, highlightbackground="black")
        canvas_frame.pack(side="left", padx=20, pady=20, expand=True)

        self.floor_img = self.app.load_image("floorplan.png", (400, 300))
        if self.floor_img:
            lbl_img = tk.Label(canvas_frame, image=self.floor_img, bg="white")
            lbl_img.image = self.floor_img
            lbl_img.pack()
        else:
            tk.Label(canvas_frame, text="[Floorplan Image Missing]", bg="white").pack(pady=50)

    def change_mode(self, mode):
        self.controller.set_security_mode(mode)

    def update_mode_display(self, text, armed_zones=None):
        self.mode_display.config(text=f"Current: {text}")
        if hasattr(self, "zones_label"):
            if armed_zones is None:
                zone_text = "Unknown"
                count = 0
            elif len(armed_zones) == 0:
                zone_text = "All Zones"
                count = 0
            else:
                zone_map = self.system.configuration_manager.get_zone_name_map()
                resolved = [zone_map.get(str(zone), str(zone)) for zone in sorted(armed_zones)]
                zone_text = ", ".join(resolved)
                count = len(armed_zones)
            self.zones_label.config(text=f"Armed Zones: {zone_text}")
            self._update_zone_indicator(count)

    def refresh(self):
        if hasattr(self.system, "security_system") and self.system.security_system:
            status = self.system.security_system.get_status()
            if status:
                text = f"{status.mode.name} ({status.alarm_state.name})"
                self.update_mode_display(text, status.armed_zones)
            else:
                self.update_mode_display(self.system.security_system.mode.name)

    def _update_zone_indicator(self, armed_count: int):
        if not hasattr(self, "zone_indicator"):
            return
        if armed_count:
            color = "#f56565"
            text = f"{armed_count} zone(s) armed"
        else:
            color = "#48bb78"
            text = "No active zones"
        self.zone_indicator.itemconfig(self.zone_indicator_id, fill=color)
        self.zone_indicator_text.config(text=text, foreground="black" if armed_count else "gray35")

class MonitoringView(ttk.Frame):
    def __init__(self, parent, system, sensors, app):
        super().__init__(parent)
        self.system = system
        self.app = app

        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome - Configuration", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: self.app.show_page("MainMenu")).pack(side="right")

        ttk.Label(self, text="Monitoring & Intrusion Log", font=("Helvetica", 16, "bold")).pack(pady=(5, 5))

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="System Settings")
        self._create_settings_tab(settings_tab)

        password_tab = ttk.Frame(notebook)
        notebook.add(password_tab, text="Change Password")
        self._create_password_tab(password_tab)

        control_tab = ttk.Frame(notebook)
        notebook.add(control_tab, text="System Control")
        self._create_control_tab(control_tab)

        ttk.Label(self, text="Intrusion Log", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))
        self.log_list = tk.Listbox(self, height=12)
        self.log_list.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.update_intrusion_log(self.app.intrusion_logs)

    def _create_settings_tab(self, parent):
        """Common Function 3: Configure system setting"""
        panel = ttk.Frame(parent, padding=20)
        panel.pack(fill="both", expand=True)

        ttk.Label(panel, text="System Settings Configuration", font=("Helvetica", 14, "bold")).pack(pady=(0, 20))

        # 현재 설정 로드
        settings = self.system.configuration_manager.get_system_setting()

        # 모니터링 서비스 전화번호
        ttk.Label(panel, text="Monitoring Service Phone:").pack(anchor="w")
        self.monitoring_phone_entry = ttk.Entry(panel, width=30)
        self.monitoring_phone_entry.insert(0, settings.get_monitoring_service_phone())
        self.monitoring_phone_entry.pack(pady=(0, 10))

        # 집주인 전화번호
        ttk.Label(panel, text="Homeowner Phone:").pack(anchor="w")
        self.homeowner_phone_entry = ttk.Entry(panel, width=30)
        self.homeowner_phone_entry.insert(0, settings.get_homeowner_phone())
        self.homeowner_phone_entry.pack(pady=(0, 10))

        # 시스템 잠금 시간
        ttk.Label(panel, text="System Lock Time (seconds):").pack(anchor="w")
        self.lock_time_entry = ttk.Entry(panel, width=30)
        self.lock_time_entry.insert(0, str(settings.get_system_lock_time()))
        self.lock_time_entry.pack(pady=(0, 10))

        # 알람 지연 시간
        ttk.Label(panel, text="Alarm Delay Time (seconds):").pack(anchor="w")
        self.alarm_delay_entry = ttk.Entry(panel, width=30)
        self.alarm_delay_entry.insert(0, str(settings.get_alarm_delay_time()))
        self.alarm_delay_entry.pack(pady=(0, 20))

        ttk.Button(panel, text="Save Settings", style="Primary.TButton",
                   command=self.save_settings).pack()

    def save_settings(self):
        """시스템 설정 저장"""
        try:
            monitoring_phone = self.monitoring_phone_entry.get()
            homeowner_phone = self.homeowner_phone_entry.get()
            lock_time = int(self.lock_time_entry.get())
            alarm_delay = int(self.alarm_delay_entry.get())

            success = self.system.configure_system_setting(
                monitoring_phone=monitoring_phone,
                homeowner_phone=homeowner_phone,
                lock_time=lock_time,
                alarm_delay=alarm_delay
            )

            if success:
                messagebox.showinfo("Success", "System settings saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save settings.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for time fields.")

    def _create_password_tab(self, parent):
        """Common Function 7: Change master password through control panel"""
        panel = ttk.Frame(parent, padding=20)
        panel.pack(fill="both", expand=True)

        ttk.Label(panel, text="Change Password", font=("Helvetica", 14, "bold")).pack(pady=(0, 20))

        # 현재 비밀번호
        ttk.Label(panel, text="Current Password:").pack(anchor="w")
        self.old_password_entry = ttk.Entry(panel, width=30, show="•")
        self.old_password_entry.pack(pady=(0, 10))

        # 새 비밀번호
        ttk.Label(panel, text="New Password:").pack(anchor="w")
        self.new_password_entry = ttk.Entry(panel, width=30, show="•")
        self.new_password_entry.pack(pady=(0, 10))

        # 새 비밀번호 확인
        ttk.Label(panel, text="Confirm New Password:").pack(anchor="w")
        self.confirm_password_entry = ttk.Entry(panel, width=30, show="•")
        self.confirm_password_entry.pack(pady=(0, 20))

        ttk.Button(panel, text="Change Password", style="Primary.TButton",
                   command=self.change_password).pack()

    def change_password(self):
        """비밀번호 변경"""
        old_pw = self.old_password_entry.get()
        new_pw = self.new_password_entry.get()
        confirm_pw = self.confirm_password_entry.get()

        if new_pw != confirm_pw:
            messagebox.showerror("Error", "New passwords do not match!")
            return

        if len(new_pw) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters long.")
            return

        # Common Function 7: Change password
        success = self.system.change_password(old_pw, new_pw)

        if success:
            messagebox.showinfo("Success", "Password changed successfully!")
            self.old_password_entry.delete(0, tk.END)
            self.new_password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to change password. Please check your current password.")

    def _create_control_tab(self, parent):
        """시스템 제어 탭"""
        panel = ttk.Frame(parent, padding=20)
        panel.pack(fill="both", expand=True)

        ttk.Label(panel, text="System Control", font=("Helvetica", 14, "bold")).pack(pady=(0, 20))

        # 시스템 상태 표시
        status_frame = ttk.Frame(panel, relief="ridge", padding=10)
        status_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(status_frame, text="System Status:", font=("Helvetica", 12, "bold")).pack(anchor="w")
        self.status_text = tk.Text(status_frame, height=6, width=50)
        self.status_text.pack()
        self.update_system_status()

        # 제어 버튼들
        btn_frame = ttk.Frame(panel)
        btn_frame.pack()

        ttk.Button(btn_frame, text="Reset System", style="Primary.TButton",
                   command=self.reset_system).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Refresh Status", style="Primary.TButton",
                   command=self.update_system_status).pack(side="left", padx=5)


    def update_intrusion_log(self, messages):
        """Refresh the intrusion log list."""
        if not hasattr(self, "log_list"):
            return
        self.log_list.delete(0, tk.END)
        if not messages:
            self.log_list.insert(tk.END, "No intrusion events yet.")
            return
        for msg in messages:
            self.log_list.insert(tk.END, msg)

    def update_system_status(self):
        """시스템 상태 업데이트"""
        if hasattr(self, 'status_text'):
            status_info = self.system.get_system_status()
            status_str = f"""System State: {status_info['state']}
Authenticated: {status_info['authenticated']}
Current User: {status_info['current_user'] or 'None'}
Security Mode: {status_info['security_mode'] or 'N/A'}
"""
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(1.0, status_str)

    def refresh(self):
        if hasattr(self.app, "intrusion_logs"):
            self.update_intrusion_log(self.app.intrusion_logs)
        self.update_system_status()

    def reset_system(self):
        """Common Function 6: Reset the system"""
        result = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the system->")
        if result:
            success = self.system.reset()
            if success:
                messagebox.showinfo("Success", "System reset successfully!")
                self.update_system_status()
            else:
                messagebox.showerror("Error", "Failed to reset system.")
