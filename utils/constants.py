# utils/constants.py
from pathlib import Path

# Security Modes
MODE_DISARMED = "Disarmed"
MODE_AWAY = "Away"
MODE_STAY = "Stay"

# Sensor Types
SENSOR_WIN_DOOR = "Window/Door Sensor"
SENSOR_MOTION = "Motion Detector"
SENSOR_CAMERA = "Camera"

# Sensor States
STATE_OPEN = "Open"
STATE_CLOSED = "Closed"
STATE_DETECTED = "Motion Detected"
STATE_CLEAR = "Clear"
STATE_RECORDING = "Recording"
STATE_IDLE = "Idle"

# DB File
DB_FILE = "safehome.db"

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if (PROJECT_ROOT / "virtual_device_v4").exists():
    VIRTUAL_DEVICE_DIR = "virtual_device_v4"
else:
    VIRTUAL_DEVICE_DIR = "virtual_device_v3"
VIRTUAL_DEVICE_PATH = PROJECT_ROOT / VIRTUAL_DEVICE_DIR
