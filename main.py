import threading
import tkinter as tk
from flask import Flask

from domain.system_controller import SystemController
from ui.main_window import SafeHomeApp
from devices.windoor_sensor import WindowDoorSensor
from devices.motion_detector import MotionDetector
from devices.camera import Camera
from utils.constants import *

app = Flask(__name__)
sys_ctrl = None

@app.route('/')
def home():
    status = sys_ctrl.current_state.get_name() if sys_ctrl else "Off"
    return f"<h1>SafeHome Web</h1><p>Status: {status}</p><a href='/arm'>Arm Away</a> | <a href='/disarm'>Disarm</a>"

@app.route('/arm')
def arm():
    if sys_ctrl and sys_ctrl.authenticated_user:
        sys_ctrl.set_security_mode(MODE_AWAY)
        return "Armed Away! <a href='/'>Back</a>"
    return "Login first on PC. <a href='/'>Back</a>"

@app.route('/disarm')
def disarm():
    if sys_ctrl:
        sys_ctrl.set_security_mode(MODE_DISARMED)
        return "Disarmed. <a href='/'>Back</a>"
    return "Error"

def run_web():
    app.run(port=5000, debug=False, use_reloader=False)

def main():
    global sys_ctrl
    root = tk.Tk()
    
    # Controller Init
    controller = SystemController()
    sys_ctrl = controller
    
    # Devices Init
    sensors = [
        WindowDoorSensor("Front Door"),
        MotionDetector("Living Room"),
        Camera("Garden Cam")
    ]
    
    # Connect Devices
    for s in sensors:
        s.add_observer(controller)
        if isinstance(s, Camera):
            controller.add_camera(s)
    
    # UI Init
    app = SafeHomeApp(root, controller, sensors)
    controller.set_ui(app)
    
    # Web Server Start
    t = threading.Thread(target=run_web, daemon=True)
    t.start()
    
    print("SafeHome System Started...")
    root.mainloop()

if __name__ == "__main__":
    main()