"""
LogManager - 로그 인스턴스 관리
이벤트 로그 저장, 조회, 검색 기능 제공
"""
from typing import List, Optional
from datetime import datetime
from event_logging.log import Log
from storage.storage_manager import StorageManager


class LogManager:
    """
    시스템 이벤트 로그를 관리하는 매니저 클래스
    """

    def __init__(self):
        self.storage = StorageManager()
        self.logs_cache: List[Log] = []  # 메모리 캐시 (선택적)

    def save_log(self, log: Log) -> bool:
        """
        로그를 데이터베이스에 저장
        :param log: Log 객체
        :return: 성공 여부
        """
        sql = """
            INSERT INTO event_logs (event_datetime, event_type, description, user_id, interface_type)
            VALUES (?, ?, ?, ?, ?)
        """

        time_str = log.get_date_time().strftime('%Y-%m-%d %H:%M:%S')
        rows = self.storage.execute_update(
            sql,
            (
                time_str,
                log.get_event_type(),
                log.get_description(),
                log.get_user_id(),
                log.get_interface_type() or 'control_panel',
            ),
        )

        if rows > 0:
            log.set_event_id(self.storage.get_last_insert_id())
            self.logs_cache.append(log)
            print(f"[LogManager] Log saved: {log.get_event_type()}")
            return True
        else:
            print(f"[LogManager] Failed to save log.")
            return False

    def log_event(
        self,
        event_type: str,
        description: str,
        user_id: str = None,
        interface_type: str = "control_panel",
    ) -> bool:
        """
        새 이벤트를 로깅 (편의 메서드)
        :param event_type: 이벤트 타입
        :param description: 이벤트 설명
        :param user_id: 사용자 ID (optional)
        :return: 성공 여부
        """
        log = Log(
            event_type=event_type,
            description=description,
            date_time=datetime.now(),
            user_id=user_id,
            interface_type=interface_type,
        )
        return self.save_log(log)

    def get_log_list(self, limit: int = 100) -> List[Log]:
        """
        최근 로그 목록 조회
        :param limit: 조회할 최대 개수
        :return: Log 객체 리스트
        """
        sql = """
            SELECT log_id, event_datetime, event_type, description, user_id, interface_type
            FROM event_logs
            ORDER BY event_datetime DESC
            LIMIT ?
        """
        result = self.storage.execute_query(sql, (limit,))

        logs = []
        if result:
            for row in result:
                log = Log(
                    event_id=row['log_id'],
                    event_type=row['event_type'],
                    description=row['description'],
                    date_time=datetime.strptime(row['event_datetime'], '%Y-%m-%d %H:%M:%S'),
                    user_id=row['user_id'],
                    interface_type=row['interface_type'],
                )
                logs.append(log)

        return logs

    def get_logs_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Log]:
        """
        날짜 범위로 로그 조회
        :param start_date: 시작 날짜
        :param end_date: 종료 날짜
        :return: Log 객체 리스트
        """
        sql = """
            SELECT log_id, event_datetime, event_type, description, user_id, interface_type
            FROM event_logs
            WHERE event_datetime BETWEEN ? AND ?
            ORDER BY event_datetime DESC
        """

        start_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
        end_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

        result = self.storage.execute_query(sql, (start_str, end_str))

        logs = []
        if result:
            for row in result:
                log = Log(
                    event_id=row['log_id'],
                    event_type=row['event_type'],
                    description=row['description'],
                    date_time=datetime.strptime(row['event_datetime'], '%Y-%m-%d %H:%M:%S'),
                    user_id=row['user_id'],
                    interface_type=row['interface_type'],
                )
                logs.append(log)

        return logs

    def get_logs_by_type(self, event_type: str, limit: int = 100) -> List[Log]:
        """
        이벤트 타입으로 로그 조회
        :param event_type: 이벤트 타입
        :param limit: 조회할 최대 개수
        :return: Log 객체 리스트
        """
        sql = """
            SELECT log_id, event_datetime, event_type, description, user_id, interface_type
            FROM event_logs
            WHERE event_type = ?
            ORDER BY event_datetime DESC
            LIMIT ?
        """
        result = self.storage.execute_query(sql, (event_type, limit))

        logs = []
        if result:
            for row in result:
                log = Log(
                    event_id=row['log_id'],
                    event_type=row['event_type'],
                    description=row['description'],
                    date_time=datetime.strptime(row['event_datetime'], '%Y-%m-%d %H:%M:%S'),
                    user_id=row['user_id'],
                    interface_type=row['interface_type'],
                )
                logs.append(log)

        return logs

    def get_logs_by_user(self, user_id: str, limit: int = 100) -> List[Log]:
        """
        사용자별 로그 조회
        :param user_id: 사용자 ID
        :param limit: 조회할 최대 개수
        :return: Log 객체 리스트
        """
        sql = """
            SELECT log_id, event_datetime, event_type, description, user_id, interface_type
            FROM event_logs
            WHERE user_id = ?
            ORDER BY event_datetime DESC
            LIMIT ?
        """
        result = self.storage.execute_query(sql, (user_id, limit))

        logs = []
        if result:
            for row in result:
                log = Log(
                    event_id=row['log_id'],
                    event_type=row['event_type'],
                    description=row['description'],
                    date_time=datetime.strptime(row['event_datetime'], '%Y-%m-%d %H:%M:%S'),
                    user_id=row['user_id'],
                    interface_type=row['interface_type'],
                )
                logs.append(log)

        return logs

    def clear_old_logs(self, days: int = 30) -> int:
        """
        오래된 로그 삭제
        :param days: 보관 기간 (일 수)
        :return: 삭제된 로그 개수
        """
        sql = """
            DELETE FROM event_logs
            WHERE event_datetime < datetime('now', '-' || ? || ' days')
        """
        rows = self.storage.execute_update(sql, (days,))

        if rows > 0:
            print(f"[LogManager] Deleted {rows} old logs (older than {days} days).")
        return rows

    def get_log_count(self) -> int:
        """전체 로그 개수 조회"""
        sql = "SELECT COUNT(*) as count FROM event_logs"
        result = self.storage.execute_query(sql)
        if result:
            return result[0]['count']
        return 0

    def __repr__(self):
        return f"LogManager(logs_in_db={self.get_log_count()}, cached={len(self.logs_cache)})"
