from __future__ import annotations

from typing import Iterable, List, Sequence

from devices.device_factory import (
    DeviceFactoryError,
    create_default_device_factory,
)
from utils.constants import (
    SENSOR_CAMERA,
    SENSOR_MOTION,
    SENSOR_WIN_DOOR,
)


class SystemBootstrapper:
    """Loads sensors from storage and wires them into the system after turn-on."""

    def __init__(self, device_factory=None):
        self.device_factory = device_factory or create_default_device_factory()

    def attach_post_turn_on_hook(self, system, ui_sensors: List):
        """Register a callback that initializes sensors once the system boots."""
        system.on_turn_on_complete = lambda: self.initialize_devices_after_turn_on(
            system, ui_sensors
        )

    def initialize_devices_after_turn_on(self, system, ui_sensors: List):
        """Refresh device objects once the system is fully initialized."""
        loaded_sensors = self.load_sensors(system)
        if loaded_sensors:
            ui_sensors.clear()
            ui_sensors.extend(loaded_sensors)
        system.sensors = ui_sensors

        controller = getattr(system, "system_controller", None)
        if controller:
            for sensor in ui_sensors:
                if hasattr(sensor, "add_observer"):
                    sensor.add_observer(controller)
                if sensor.get_type() == SENSOR_CAMERA and hasattr(sensor, "take_picture"):
                    controller.add_camera(sensor)
            print("[Bootstrap] Connected sensors to SystemController")

        camera_controller = getattr(system, "camera_controller", None)
        if camera_controller:
            for coords in ((350, 20), (330, 208), (332, 262)):
                camera_controller.add_camera(*coords)
            print(
                "[Bootstrap] Initialized 3 cameras in CameraController at predefined positions"
            )

    def load_sensors(self, system) -> List:
        """Instantiate sensor objects from the persisted catalog (with fallback defaults)."""
        config = getattr(system, "configuration_manager", None)
        device_records: Sequence[tuple] = []

        if config and getattr(config, "device_manager", None):
            try:
                device_records = config.device_manager.load_all_devices()
            except Exception as exc:  # pragma: no cover - defensive
                print(f"[Bootstrap] Failed to load devices from database: {exc}")

        sensors = self._instantiate_devices(device_records)
        if sensors:
            return sensors

        fallback_reason = (
            "System configuration unavailable" if not config else "No registered devices available"
        )
        print(f"[Bootstrap] {fallback_reason}; using fallback defaults.")
        fallback_records = [
            ("Front Door", SENSOR_WIN_DOOR),
            ("Living Room", SENSOR_MOTION),
            ("Garden Cam", SENSOR_CAMERA),
        ]

        return self._instantiate_devices(fallback_records)

    def _instantiate_devices(self, records: Iterable[tuple]) -> List:
        sensors: List = []
        for device_id, device_type in records:
            try:
                sensors.append(self.device_factory.create(device_type, device_id))
            except DeviceFactoryError as exc:
                print(f"[Bootstrap] Skipping device '{device_id}': {exc}")
        return sensors
