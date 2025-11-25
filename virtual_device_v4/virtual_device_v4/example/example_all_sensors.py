#!/usr/bin/env python3
"""
All Sensors Example
===================
This example demonstrates both Window/Door Sensors and Motion Detectors
with their respective functionalities in a single GUI.

Usage:
    python -m example.example_all_sensors
    OR
    python example_all_sensors.py (when run from example directory)
"""

import sys
from pathlib import Path

# Add parent directory to path for direct script execution
if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))

# Try relative import first (for package execution), fall back to absolute
try:
    from device.device_windoor_sensor import DeviceWinDoorSensor
    from device.device_motion_detector import DeviceMotionDetector
    from device.device_sensor_tester import DeviceSensorTester
except ImportError:
    from ..device.device_windoor_sensor import DeviceWinDoorSensor
    from ..device.device_motion_detector import DeviceMotionDetector
    from ..device.device_sensor_tester import DeviceSensorTester


def main():
    """Test creating multiple window/door sensors and motion detectors."""
    # Ensure GUI is initialized (will be None in headless or when tkinter unavailable)
    DeviceSensorTester.showSensorTester()
    print("=" * 60)
    print("SafeHome Sensor Test - All Sensors")
    print("=" * 60)
    
    # Create Window/Door Sensors
    print("\n[1] Creating Window/Door sensors...")
    wd_sensor1 = DeviceWinDoorSensor()
    print(f"    ✓ WinDoor Sensor 1 created with ID: {wd_sensor1.get_id()}")
    
    wd_sensor2 = DeviceWinDoorSensor()
    print(f"    ✓ WinDoor Sensor 2 created with ID: {wd_sensor2.get_id()}")
    
    wd_sensor3 = DeviceWinDoorSensor()
    print(f"    ✓ WinDoor Sensor 3 created with ID: {wd_sensor3.get_id()}")
    
    # arm Window/Door sensors
    wd_sensor1.arm()
    wd_sensor2.arm()
    wd_sensor3.arm()
    print("    ✓ All Window/Door sensors armed!")
    
    # Create Motion Detectors
    print("\n[2] Creating Motion Detector sensors...")
    motion1 = DeviceMotionDetector()
    print(f"    ✓ Motion Detector 1 created with ID: {motion1.get_id()}")
    
    motion2 = DeviceMotionDetector()
    print(f"    ✓ Motion Detector 2 created with ID: {motion2.get_id()}")
    
    motion3 = DeviceMotionDetector()
    print(f"    ✓ Motion Detector 3 created with ID: {motion3.get_id()}")
    
    # arm Motion detectors
    motion1.arm()
    motion2.arm()
    motion3.arm()
    print("    ✓ All Motion detectors armed!")
    
    # Display initial states
    print("\n" + "=" * 60)
    print("Initial Sensor States:")
    print("-" * 60)
    print(f"Window/Door Sensors: S1={wd_sensor1.read()}, S2={wd_sensor2.read()}, S3={wd_sensor3.read()}")
    print(f"Motion Detectors:    D1={motion1.read()}, D2={motion2.read()}, D3={motion3.read()}")
    print("=" * 60)
    
    # Display test instructions
    print("\n📋 Test Instructions:")
    print("\n  Window/Door Sensors (IDs: 1-3):")
    print("    • Enter sensor ID in the left panel")
    print("    • Click 'open' to simulate opening")
    print("    • Click 'close' to simulate closing")
    print("\n  Motion Detectors (IDs: 1-3):")
    print("    • Enter detector ID in the right panel")
    print("    • Click 'detect' to simulate motion")
    print("    • Click 'clear' to clear detection")
    print("\n" + "=" * 60)
    
    # Update GUI with sensor ID ranges
    gui = DeviceSensorTester.safeHomeSensorTest
    if gui:
        gui.rangeSensorID_WinDoorSensor.set(f"{wd_sensor1.get_id()}-{wd_sensor3.get_id()}")
        gui.rangeSensorID_MotionDetector.set(f"{motion1.get_id()}-{motion3.get_id()}")
        print("✅ GUI initialized successfully! Starting main loop...")
        print("=" * 60)
        gui.mainloop()
    else:
        print("⚠️  Warning: GUI not initialized (running in headless mode or tkinter not available)")


if __name__ == "__main__":
    main()
