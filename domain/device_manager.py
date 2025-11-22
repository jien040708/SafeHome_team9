from storage.storage_manager import StorageManager
from utils.constants import *

class DeviceManager:
    def __init__(self):
        self.storage = StorageManager()
        self._initialize_table()

    def _initialize_table(self):
        # StorageManager를 통해 테이블 생성
        sql = """
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                device_type TEXT
            )
        """
        # execute_update는 commit을 포함함
        self.storage.execute_update(sql)
        
        # 초기 데이터 확인 및 생성
        result = self.storage.execute_query("SELECT count(*) as cnt FROM devices")
        count = result[0]['cnt'] if result else 0
        
        if count == 0:
            print("[DeviceManager] Initializing default devices...")
            self.add_device("Front Door", SENSOR_WIN_DOOR)
            self.add_device("Living Room", SENSOR_MOTION)
            self.add_device("Garden Cam", SENSOR_CAMERA)

    def add_device(self, d_id, d_type):
        sql = "INSERT INTO devices (device_id, device_type) VALUES (?, ?)"
        res = self.storage.execute_update(sql, (d_id, d_type))
        return res > 0

    def remove_device(self, d_id):
        sql = "DELETE FROM devices WHERE device_id = ?"
        res = self.storage.execute_update(sql, (d_id,))
        return res > 0

    def load_all_devices(self):
        """(id, type) 튜플 리스트 반환"""
        sql = "SELECT device_id, device_type FROM devices"
        rows = self.storage.execute_query(sql)
        if rows:
            return [(r['device_id'], r['device_type']) for r in rows]
        return []