from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from storage.storage_manager import StorageManager
from utils.constants import *


class DeviceManager:
    """Gateway that persists device metadata and sensor-to-zone assignments."""

    def __init__(self) -> None:
        self.storage = StorageManager()
        self._initialize_tables()

    def _initialize_tables(self) -> None:
        """Ensure device and assignment tables exist and seed defaults."""
        device_sql = """
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                device_type TEXT NOT NULL
            )
        """
        self.storage.execute_update(device_sql)

        result = self.storage.execute_query("SELECT count(*) as cnt FROM devices")
        count = result[0]['cnt'] if result else 0

        if count == 0:
            print("[DeviceManager] Initializing default devices...")
            self.add_device("Front Door", SENSOR_WIN_DOOR)
            self.add_device("Living Room", SENSOR_MOTION)
            self.add_device("Garden Cam", SENSOR_CAMERA)

    def add_device(self, device_id: str, device_type: str) -> bool:
        sql = "INSERT INTO devices (device_id, device_type) VALUES (?, ?)"
        res = self.storage.execute_update(sql, (device_id, device_type))
        return res > 0

    def remove_device(self, device_id: str) -> bool:
        sql = "DELETE FROM devices WHERE device_id = ?"
        res = self.storage.execute_update(sql, (device_id,))
        if res > 0:
            self.remove_device_zone_assignment(device_id)
        return res > 0

    def load_all_devices(self) -> List[Tuple[str, str]]:
        """Return the list of (device_id, device_type)."""
        sql = "SELECT device_id, device_type FROM devices"
        rows = self.storage.execute_query(sql)
        if rows:
            return [(r['device_id'], r['device_type']) for r in rows]
        return []

    def load_device_zone_assignments(self) -> Dict[str, int]:
        """Return mapping of device -> zone id."""
        sql = "SELECT device_id, zone_id FROM sensor_zone_assignments"
        rows = self.storage.execute_query(sql)
        if not rows:
            return {}
        return {row['device_id']: row['zone_id'] for row in rows}

    def get_device_zone(self, device_id: str) -> Optional[int]:
        sql = "SELECT zone_id FROM sensor_zone_assignments WHERE device_id = ?"
        rows = self.storage.execute_query(sql, (device_id,))
        if rows:
            return rows[0]['zone_id']
        return None

    def assign_device_to_zone(self, device_id: str, zone_id: int) -> bool:
        """Create or update a zone assignment for a sensor."""
        sql = """
            INSERT INTO sensor_zone_assignments (device_id, zone_id)
            VALUES (?, ?)
            ON CONFLICT(device_id) DO UPDATE SET zone_id = excluded.zone_id,
                                               assigned_at = CURRENT_TIMESTAMP
        """
        res = self.storage.execute_update(sql, (device_id, zone_id))
        return res > 0

    def remove_device_zone_assignment(self, device_id: str) -> bool:
        sql = "DELETE FROM sensor_zone_assignments WHERE device_id = ?"
        res = self.storage.execute_update(sql, (device_id,))
        return res > 0
