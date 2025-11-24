from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Tuple

from interfaces.sensor_interface import ISensor
from utils.constants import SENSOR_CAMERA, SENSOR_MOTION, SENSOR_WIN_DOOR

FactoryFn = Callable[[str], ISensor]


class DeviceFactoryError(RuntimeError):
    """Raised when the factory cannot fulfill a creation request."""


@dataclass(frozen=True)
class RegisteredDevice:
    """Simple data holder describing a registered device builder."""

    device_type: str
    builder: FactoryFn


class DeviceFactory:
    """Registry backed factory for SafeHome sensor devices."""

    def __init__(self) -> None:
        self._registry: Dict[str, FactoryFn] = {}

    def register(self, device_type: str, builder: FactoryFn, *, override: bool = False) -> None:
        """Register a device builder callable for the given type string."""
        normalized = self._normalize_type(device_type)
        if not callable(builder):
            raise ValueError("builder must be callable")
        if normalized in self._registry and not override:
            raise DeviceFactoryError(f"Device type '{normalized}' is already registered")
        self._registry[normalized] = builder

    def unregister(self, device_type: str) -> None:
        """Remove a registered device builder."""
        normalized = self._normalize_type(device_type)
        self._registry.pop(normalized, None)

    def create(self, device_type: str, device_id: str) -> ISensor:
        """Instantiate a device of the requested type."""
        normalized = self._normalize_type(device_type)
        try:
            builder = self._registry[normalized]
        except KeyError as exc:
            raise DeviceFactoryError(f"No device registered for type '{normalized}'") from exc

        sensor = builder(device_id)
        if not isinstance(sensor, ISensor):
            raise DeviceFactoryError(
                f"Builder for '{normalized}' must return an ISensor instance"
            )
        return sensor

    def build_many(self, records: Iterable[Tuple[str, str]]) -> List[ISensor]:
        """Create sensors for the provided (device_id, device_type) records."""
        sensors: List[ISensor] = []
        for device_id, device_type in records:
            sensors.append(self.create(device_type, device_id))
        return sensors

    def registered_devices(self) -> List[RegisteredDevice]:
        """Return a snapshot of the registered device builders."""
        return [
            RegisteredDevice(device_type=device_type, builder=builder)
            for device_type, builder in self._registry.items()
        ]

    @staticmethod
    def _normalize_type(device_type: str) -> str:
        if not isinstance(device_type, str):
            raise ValueError("device_type must be a string")
        normalized = device_type.strip()
        if not normalized:
            raise ValueError("device_type must be non-empty")
        return normalized


def register_builtin_devices(factory: DeviceFactory) -> DeviceFactory:
    """Populate the provided factory with the core SafeHome sensors."""
    # Lazy imports keep the factory decoupled from module initialization order.
    from devices.camera import Camera
    from devices.motion_detector import MotionDetector
    from devices.windoor_sensor import WindowDoorSensor

    factory.register(SENSOR_WIN_DOOR, WindowDoorSensor, override=True)
    factory.register(SENSOR_MOTION, MotionDetector, override=True)
    factory.register(SENSOR_CAMERA, Camera, override=True)
    return factory


def create_default_device_factory() -> DeviceFactory:
    """Convenience helper that returns a factory loaded with built-in sensors."""
    factory = DeviceFactory()
    return register_builtin_devices(factory)
