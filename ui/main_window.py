import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from utils.constants import *

# 페이지 이름 상수
PAGES = ("Login", "MainMenu", "Zones", "Modes", "Monitoring")

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
        self.images = {} # 이미지 참조 유지용

        # 각 페이지 뷰 생성
        for page_name in PAGES:
            cls = globals()[f"{page_name}View"]
            # app=self를 전달하여 뷰에서 SafeHomeApp 메서드 호출 가능하게 함
            frame = cls(parent=container, system=self.system, sensors=self.sensors, app=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # 하단 상태바 생성
        self.create_status_bar()

        # 초기 화면
        self.show_page("Login")

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

    def update_status_label(self, text):
        self.status_label.config(text=f"Status: {text}")
        # Modes 화면의 상태 텍스트도 함께 갱신
        if "Modes" in self.frames:
            self.frames["Modes"].update_mode_display(text)

    def add_log(self, message):
        current = self.status_label.cget("text")
        if len(current) > 80: current = current[:80] + "..."
        self.status_label.config(text=f"{current} | {message}")

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


# --- View Classes (기존 UI 디자인 반영) ---

class LoginView(ttk.Frame):
    def __init__(self, parent, system, sensors, app):
        super().__init__(parent)
        self.system = system
        self.app = app

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
                   command=self.attempt_login).pack()

    def attempt_login(self):
        uid = self.user_entry.get()
        pw = self.pass_entry.get()
        # Common Function 1: Log onto the system through control panel
        if self.system.login(uid, pw, interface='control_panel'):
            self.app.show_page("MainMenu")
        else:
            messagebox.showerror("Login Failed", "Invalid ID or Password")


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
        self.app = app
        self.sensors = sensors

        # 헤더 영역
        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: self.app.show_page("MainMenu")).pack(side="right")

        # 좌측 패널 (센서 제어)
        nav = ttk.Frame(self)
        nav.pack(side="left", fill="y", padx=10, pady=10)
        
        # 더미 버튼들 (디자인 유지)
        for label in ["Add Safety zone", "Update Safety zone", "Delete Safety zone"]:
            ttk.Button(nav, text=label, style="Primary.TButton").pack(pady=5, fill="x")

        ttk.Label(nav, text="Sensor Simulation", font=("Helvetica", 12, "bold")).pack(pady=(20, 5))
        
        # 실제 센서 트리거 버튼 생성
        for s in self.sensors:
            f = ttk.Frame(nav)
            f.pack(fill="x", pady=2)
            ttk.Label(f, text=s.get_id(), width=15).pack(side="left")
            ttk.Button(f, text="Trigger", width=8,
                       command=lambda sensor=s: self.trigger_sensor(sensor)).pack(side="right")

        # 우측 캔버스 영역 (이미지 적용)
        canvas_frame = tk.Frame(self, bg="white", highlightthickness=2, highlightbackground="black")
        canvas_frame.pack(side="left", padx=20, pady=20, expand=True)

        # [수정 2] floorplan.png 이미지 로드
        self.floor_img = self.app.load_image("floorplan.png", (400, 300))
        if self.floor_img:
            lbl_img = tk.Label(canvas_frame, image=self.floor_img, bg="white")
            lbl_img.image = self.floor_img # 참조 유지
            lbl_img.pack()
        else:
            tk.Label(canvas_frame, text="[Floorplan Image Missing]", bg="white").pack(pady=50)
            
        tk.Label(canvas_frame, text="First Floor Layout", font=("Helvetica", 10, "italic"), bg="white").pack(pady=5)

    def trigger_sensor(self, sensor):
        if "Window" in sensor.get_type(): sensor.set_open()
        elif "Motion" in sensor.get_type(): sensor.detect_motion()
        messagebox.showinfo("Sensor", f"{sensor.get_id()} Triggered!")


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
        
        # 모드 설정 버튼 (실제 기능 연결)
        modes = [("Arm Away", MODE_AWAY), ("Arm Stay", MODE_STAY), ("Disarm", MODE_DISARMED)]
        for label, mode_const in modes:
            ttk.Button(nav, text=label, style="Primary.TButton",
                       command=lambda m=mode_const: self.change_mode(m)).pack(pady=5, fill="x")
            
        # 더미 버튼들
        for label in ["Overnight Travel", "Guest Home"]:
            ttk.Button(nav, text=label, style="Primary.TButton").pack(pady=5, fill="x")
            
        # 상태 표시 라벨
        self.mode_display = ttk.Label(nav, text="Current: Disarmed", font=("Helvetica", 14, "bold"), foreground="blue")
        self.mode_display.pack(pady=20)

        # 우측 캔버스 (이미지 재사용)
        canvas_frame = tk.Frame(self, bg="white", highlightthickness=2, highlightbackground="black")
        canvas_frame.pack(side="left", padx=20, pady=20, expand=True)

        # [수정 2] floorplan.png 이미지 로드 (크기 조절)
        self.floor_img = self.app.load_image("floorplan.png", (400, 300))
        if self.floor_img:
            lbl_img = tk.Label(canvas_frame, image=self.floor_img, bg="white")
            lbl_img.image = self.floor_img
            lbl_img.pack()
        else:
            tk.Label(canvas_frame, text="[Floorplan Image Missing]", bg="white").pack(pady=50)

    def change_mode(self, mode):
        self.controller.set_security_mode(mode)

    def update_mode_display(self, text):
        # [수정 3] 상태 업데이트 버그 해결 (라벨 텍스트 변경)
        self.mode_display.config(text=f"Current: {text}")
        
    def refresh(self):
        # 화면이 열릴 때 최신 상태 반영
        current_status = self.controller.current_state.get_name()
        self.update_mode_display(current_status)


class MonitoringView(ttk.Frame):
    def __init__(self, parent, system, sensors, app):
        super().__init__(parent)
        self.system = system
        self.app = app

        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome - Configuration", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: self.app.show_page("MainMenu")).pack(side="right")

        # 탭 형태로 구성
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab 1: 시스템 설정 (Common Function 3)
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="System Settings")
        self._create_settings_tab(settings_tab)

        # Tab 2: 비밀번호 변경 (Common Function 7)
        password_tab = ttk.Frame(notebook)
        notebook.add(password_tab, text="Change Password")
        self._create_password_tab(password_tab)

        # Tab 3: 시스템 제어
        control_tab = ttk.Frame(notebook)
        notebook.add(control_tab, text="System Control")
        self._create_control_tab(control_tab)

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

    def reset_system(self):
        """Common Function 6: Reset the system"""
        result = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the system?")
        if result:
            success = self.system.reset()
            if success:
                messagebox.showinfo("Success", "System reset successfully!")
                self.update_system_status()
            else:
                messagebox.showerror("Error", "Failed to reset system.")