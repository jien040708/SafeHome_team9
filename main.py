import threading
import tkinter as tk
from flask import Flask

from domain.system import System
from ui.main_window import SafeHomeApp
from devices.windoor_sensor import WindowDoorSensor
from devices.motion_detector import MotionDetector
from devices.camera import Camera
from utils.constants import *

app = Flask(__name__)
safehome_system = None

@app.route('/')
def home():
    if safehome_system and safehome_system.system_controller:
        status = safehome_system.system_controller.current_state.get_name()
        user = safehome_system.login_manager.get_current_user()
        user_info = f"Logged in as: {user.get_username()}" if user else "Not logged in"
    else:
        status = "Off"
        user_info = "System offline"

    return f"""
    <h1>SafeHome Web Interface</h1>
    <p>Status: {status}</p>
    <p>{user_info}</p>
    <hr>
    <a href='/arm'>Arm Away</a> | <a href='/disarm'>Disarm</a>
    <br><br>
    <a href='/status'>System Status</a>
    """

@app.route('/arm')
def arm():
    if safehome_system and safehome_system.login_manager.is_user_authenticated():
        safehome_system.system_controller.set_security_mode(MODE_AWAY)
        return "Armed Away! <a href='/'>Back</a>"
    return "Please login first on Control Panel. <a href='/'>Back</a>"

@app.route('/disarm')
def disarm():
    if safehome_system and safehome_system.system_controller:
        safehome_system.system_controller.set_security_mode(MODE_DISARMED)
        return "Disarmed. <a href='/'>Back</a>"
    return "Error <a href='/'>Back</a>"

@app.route('/status')
def status():
    if safehome_system:
        status_info = safehome_system.get_system_status()
        return f"""
        <h2>System Status</h2>
        <ul>
            <li>State: {status_info['state']}</li>
            <li>Authenticated: {status_info['authenticated']}</li>
            <li>Current User: {status_info['current_user']}</li>
            <li>Security Mode: {status_info['security_mode']}</li>
        </ul>
        <a href='/'>Back</a>
        """
    return "System offline <a href='/'>Back</a>"

def run_web():
    app.run(port=5000, debug=False, use_reloader=False)

def main():
    global safehome_system
    root = tk.Tk()

    # System Init (Common Function 4: Turn the system on)
    safehome_system = System()
    if not safehome_system.turn_on():
        print("Failed to start SafeHome system. Exiting...")
        return

    # Devices Init
    sensors = [
        WindowDoorSensor("Front Door"),
        MotionDetector("Living Room"),
        Camera("Garden Cam")
    ]

    # Connect Devices to SystemController
    if safehome_system.system_controller:
        for s in sensors:
            s.add_observer(safehome_system.system_controller)
            if isinstance(s, Camera):
                safehome_system.system_controller.add_camera(s)

    # UI Init
    ui_app = SafeHomeApp(root, safehome_system, sensors)
    safehome_system.set_ui(ui_app)

    # Web Server Start
    t = threading.Thread(target=run_web, daemon=True)
    t.start()

    print("=" * 50)
    print("SafeHome System Started Successfully!")
    print("Control Panel: Running on Tkinter window")
    print("Web Interface: http://localhost:5000")
    print("=" * 50)

    try:
        root.mainloop()
    finally:
        # System Shutdown (Common Function 5: Turn the system off)
        print("\nShutting down SafeHome system...")
        safehome_system.turn_off()

if __name__ == "__main__":
    main()