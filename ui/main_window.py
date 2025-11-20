import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from utils.constants import *

# 페이지 이름 상수
PAGES = ("Login", "MainMenu", "Zones", "Modes", "Monitoring")

class SafeHomeApp:
    def __init__(self, root, controller, sensors):
        self.root = root
        self.controller = controller
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
            frame = cls(parent=container, controller=self.controller, sensors=self.sensors, app=self)
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
    def __init__(self, parent, controller, sensors, app):
        super().__init__(parent)
        self.controller = controller
        self.app = app
        
        ttk.Label(self, text="SafeHome", style="Title.TLabel").pack(pady=(40, 30))
        
        panel = ttk.Frame(self, padding=30, relief="groove")
        panel.pack()
        
        ttk.Label(panel, text="LOGIN SAFEHOME SYSTEM", font=("Helvetica", 12, "bold")).pack(pady=(0, 20))
        
        self.user_entry = ttk.Entry(panel, width=30)
        self.pass_entry = ttk.Entry(panel, width=30, show="•")
        
        ttk.Label(panel, text="User ID").pack(anchor="w")
        self.user_entry.pack(pady=(0, 10))
        # [수정 1] 자동 입력 제거 (빈 칸으로 시작)
        
        ttk.Label(panel, text="Password").pack(anchor="w")
        self.pass_entry.pack(pady=(0, 20))
        
        ttk.Button(panel, text="LOGIN", style="Primary.TButton",
                   command=self.attempt_login).pack()

    def attempt_login(self):
        uid = self.user_entry.get()
        pw = self.pass_entry.get()
        if self.controller.login(uid, pw):
            self.app.show_page("MainMenu")
        else:
            messagebox.showerror("Login Failed", "Invalid ID or Password")


class MainMenuView(ttk.Frame):
    def __init__(self, parent, controller, sensors, app):
        super().__init__(parent)
        self.app = app
        
        ttk.Label(self, text="SafeHome", style="Title.TLabel").pack(pady=(40, 30))
        
        # 메뉴 버튼들
        for target, label in [("Zones", "SECURITY"), ("Modes", "SURVEILLANCE"), ("Monitoring", "CONFIGURE")]:
            ttk.Button(self, text=label, style="Primary.TButton",
                       command=lambda t=target: self.app.show_page(t)).pack(pady=10, ipadx=30)
            
        ttk.Button(self, text="LOGOUT", 
                   command=lambda: self.app.show_page("Login")).pack(pady=20)


class ZonesView(ttk.Frame):
    def __init__(self, parent, controller, sensors, app):
        super().__init__(parent)
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
    def __init__(self, parent, controller, sensors, app):
        super().__init__(parent)
        self.controller = controller
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
    def __init__(self, parent, controller, sensors, app):
        super().__init__(parent)
        self.app = app
        
        header = ttk.Frame(self)
        header.pack(fill="x", pady=10, padx=10)
        ttk.Label(header, text="SafeHome", style="Title.TLabel").pack(side="left")
        ttk.Button(header, text="Back", command=lambda: self.app.show_page("MainMenu")).pack(side="right")

        # 툴바 (디자인용)
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", padx=10)
        for label in ["Access", "Configure", "System Status", "View", "Monitoring"]:
            ttk.Button(toolbar, text=label).pack(side="left", padx=5)

        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)

        # 좌측 제어 패널
        left = ttk.Frame(main)
        left.pack(side="left", fill="y", padx=(0, 10))
        ttk.Label(left, text="RECORDING").pack(anchor="w")
        for label in ["BEGIN", "STOP", "SHOW"]:
            ttk.Button(left, text=label, style="Primary.TButton").pack(fill="x", pady=3)

        # 모니터링 영역 (카메라 이미지 표시)
        monitor_area = ttk.Frame(main)
        monitor_area.pack(fill="both", expand=True, pady=10)
        
        # [수정 2] 카메라 이미지 3개 로드 및 배치
        cam_files = ["camera1.jpg", "camera2.jpg", "camera3.jpg"]
        self.cam_photos = []

        # 그리드 레이아웃 사용
        for i, cam_file in enumerate(cam_files):
            frame = ttk.Frame(monitor_area, padding=5, relief="ridge")
            # 2열로 배치 (0, 1번은 윗줄, 2번은 아랫줄)
            row = 0 if i < 2 else 1
            col = i % 2
            frame.grid(row=row, column=col, padx=10, pady=10)
            
            photo = self.app.load_image(cam_file, (200, 150))
            if photo:
                lbl = tk.Label(frame, image=photo)
                lbl.image = photo # 참조 유지
                self.cam_photos.append(photo)
                lbl.pack()
            else:
                tk.Label(frame, text=f"[No Image]\n{cam_file}", width=25, height=10, bg="black", fg="white").pack()
            
            ttk.Label(frame, text=f"Camera {i+1} - Live").pack()

        # 슬라이더 (디자인용)
        sliders = ttk.Frame(monitor_area)
        sliders.grid(row=1, column=1, pady=10) # 우측 하단 배치
        ttk.Label(sliders, text="Zoom").pack(anchor="w")
        tk.Scale(sliders, from_=0, to=10, orient="horizontal").pack()
        ttk.Label(sliders, text="Pan").pack(anchor="w")
        tk.Scale(sliders, from_=0, to=10, orient="horizontal").pack()