from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ZoneDisplay:
    zone_id: int
    zone_name: str

    @property
    def label(self) -> str:
        return f"[{self.zone_id}] {self.zone_name}"


class ZonesViewModel:
    """View-model that mediates between the UI and configuration manager."""

    def __init__(self, system):
        self.system = system

    @property
    def config_manager(self):
        return getattr(self.system, "configuration_manager", None)

    def get_zones(self) -> List[ZoneDisplay]:
        config = self.config_manager
        if not config:
            return []
        zones = config.refresh_safety_zones()
        return [ZoneDisplay(zone.zone_id, zone.zone_name) for zone in zones]

    def get_sensor_ids(self) -> List[str]:
        config = self.config_manager
        if not config or not getattr(config, "device_manager", None):
            return []
        devices = config.device_manager.load_all_devices()
        return [device_id for device_id, _ in devices]

    def get_sensor_zone_map(self) -> dict:
        config = self.config_manager
        if not config:
            return {}
        assignments = config.list_sensor_assignments()
        zone_map = config.get_zone_name_map()
        return {
            sensor_id: zone_map.get(str(zone_id), str(zone_id))
            for sensor_id, zone_id in assignments.items()
        }

    def add_zone(self, name: str) -> bool:
        config = self.config_manager
        if not config or not name:
            return False
        return bool(config.add_safety_zone(name))

    def rename_zone(self, zone_id: int, name: str) -> bool:
        config = self.config_manager
        if not config or zone_id is None or not name:
            return False
        config.modify_safety_zone(zone_id, zone_name=name)
        return True

    def delete_zone(self, zone_id: int) -> bool:
        config = self.config_manager
        if not config or zone_id is None:
            return False
        config.delete_safety_zone(zone_id)
        return True

    def assign_sensor(self, sensor_id: str, zone_id: int) -> bool:
        config = self.config_manager
        if not config or not sensor_id or zone_id is None:
            return False
        return bool(config.assign_sensor_to_zone(sensor_id, zone_id))

    def clear_assignment(self, sensor_id: str) -> bool:
        config = self.config_manager
        if not config or not sensor_id:
            return False
        return bool(config.remove_sensor_assignment(sensor_id))
