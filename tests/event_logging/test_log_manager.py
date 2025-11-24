from __future__ import annotations

from datetime import datetime, timedelta
import sqlite3

from event_logging.log import Log
from event_logging.log_manager import LogManager


class StubStorage:
    def __init__(self):
        self.executed_updates = []
        self.executed_queries = []
        self.update_result = 1
        self.query_result = []
        self.last_insert_id = 99
        self.connect_calls = 0

    def execute_update(self, sql, params=()):
        self.executed_updates.append((sql.strip(), params))
        return self.update_result

    def execute_query(self, sql, params=()):
        self.executed_queries.append((sql.strip(), params))
        return self.query_result

    def get_last_insert_id(self):
        return self.last_insert_id

    def connect(self):
        self.connect_calls += 1


def make_log(event_type="TEST", description="desc", ts=None):
    return Log(
        event_type=event_type,
        description=description,
        date_time=ts or datetime(2025, 1, 1, 12, 0, 0),
        user_id="user-1",
        interface_type="control_panel",
    )


def test_save_log_success_sets_event_id_and_cache():
    storage = StubStorage()
    manager = LogManager(storage=storage)
    log = make_log()

    assert manager.save_log(log)
    assert log.get_event_id() == storage.last_insert_id
    assert manager.logs_cache[-1] is log

    _, params = storage.executed_updates[-1]
    assert params[1] == "TEST"
    assert params[3] == "user-1"
    assert params[4] == "control_panel"


def test_save_log_failure_when_storage_returns_zero():
    storage = StubStorage()
    storage.update_result = 0
    manager = LogManager(storage=storage)
    log = make_log()

    assert not manager.save_log(log)
    assert manager.logs_cache == []


def test_log_event_builds_log_with_defaults():
    storage = StubStorage()
    manager = LogManager(storage=storage)

    assert manager.log_event("ALARM", "Triggered")
    _, params = storage.executed_updates[-1]
    assert params[1] == "ALARM"
    assert params[-1] == "control_panel"


def test_log_event_respects_custom_interface_and_user():
    storage = StubStorage()
    manager = LogManager(storage=storage)

    assert manager.log_event("RESET", "Manual reset", user_id="ops", interface_type="web")
    _, params = storage.executed_updates[-1]
    assert params[3] == "ops"
    assert params[-1] == "web"


def _row(**overrides):
    base = {
        "log_id": 1,
        "event_datetime": "2025-01-01 12:00:00",
        "event_type": "TEST",
        "description": "desc",
        "user_id": "user-1",
        "interface_type": "control_panel",
    }
    base.update(overrides)
    return base


def test_get_log_list_converts_rows_to_log_objects():
    storage = StubStorage()
    storage.query_result = [_row(log_id=5, event_type="ALARM")]
    manager = LogManager(storage=storage)

    logs = manager.get_log_list(limit=10)
    assert len(logs) == 1
    assert logs[0].get_event_id() == 5
    assert logs[0].get_event_type() == "ALARM"
    assert logs[0].get_user_id() == "user-1"


def test_get_log_list_handles_empty_results():
    storage = StubStorage()
    storage.query_result = None  # simulate DB failure
    manager = LogManager(storage=storage)

    assert manager.get_log_list() == []


def test_get_logs_by_date_range_uses_boundaries():
    storage = StubStorage()
    storage.query_result = [_row()]
    manager = LogManager(storage=storage)
    start = datetime(2025, 1, 1, 0, 0, 0)
    end = start + timedelta(days=1)

    result = manager.get_logs_by_date_range(start, end)
    assert len(result) == 1
    _, params = storage.executed_queries[-1]
    assert params == (
        "2025-01-01 00:00:00",
        "2025-01-02 00:00:00",
    )


def test_get_logs_by_type_and_user_apply_filters():
    storage = StubStorage()
    manager = LogManager(storage=storage)

    manager.get_logs_by_type("ALARM", limit=5)
    manager.get_logs_by_user("operator", limit=7)

    assert ("ALARM", 5) == storage.executed_queries[-2][1]
    assert ("operator", 7) == storage.executed_queries[-1][1]


def test_clear_old_logs_returns_deleted_count():
    storage = StubStorage()
    storage.update_result = 3
    manager = LogManager(storage=storage)

    assert manager.clear_old_logs(days=90) == 3
    assert storage.executed_updates[-1][1] == (90,)


def test_get_log_count_and_repr():
    storage = StubStorage()
    storage.query_result = [{"count": 4}]
    manager = LogManager(storage=storage)
    manager.logs_cache.extend([make_log(), make_log()])

    assert manager.get_log_count() == 4
    summary = repr(manager)
    assert "logs_in_db=4" in summary
    assert "cached=2" in summary


def test_save_log_retries_after_failure():
    class FlakyStorage(StubStorage):
        def __init__(self):
            super().__init__()
            self.calls = 0

        def execute_update(self, sql, params=()):
            self.calls += 1
            if self.calls == 1:
                return -1  # simulate failed write
            return super().execute_update(sql, params)

    storage = FlakyStorage()
    manager = LogManager(storage=storage)
    log = make_log()

    assert manager.save_log(log)
    assert storage.connect_calls == 1  # retried once
    assert storage.calls == 2


def test_save_log_handles_sqlite_errors():
    class ErrorStorage(StubStorage):
        def execute_update(self, sql, params=()):
            raise sqlite3.OperationalError("db locked")

    storage = ErrorStorage()
    manager = LogManager(storage=storage)

    log = make_log()
    assert not manager.save_log(log)
    # connect should be attempted once between retries
    assert storage.connect_calls == 1
