from datetime import datetime

from event_logging.log import Log


def test_to_dict_formats_datetime():
    ts = datetime(2025, 1, 1, 12, 0, 0)
    log = Log(
        event_id=42,
        event_type="ALARM",
        description="Door opened",
        date_time=ts,
        user_id="admin",
        interface_type="control_panel",
    )
    data = log.to_dict()
    assert data["event_id"] == 42
    assert data["event_type"] == "ALARM"
    assert data["date_time"] == "2025-01-01 12:00:00"


def test_string_representation_includes_optional_fields():
    ts = datetime(2025, 1, 1, 8, 30, 0)
    log = Log(
        event_id=1,
        event_type="RESET",
        description="System reset",
        date_time=ts,
        user_id="operator",
        interface_type="web",
    )
    text = str(log)
    assert "System reset" in text
    assert "[User: operator]" in text
    assert "[web]" in text


def test_repr_contains_core_fields():
    log = Log(event_id=7, event_type="TEST", description="desc", date_time=datetime(2025, 1, 1))
    output = repr(log)
    assert "Log(" in output
    assert "type=TEST" in output


def test_setters_and_getters_work():
    log = Log()
    log.set_event_id(10)
    log.set_event_type("CHANGE")
    log.set_description("Updated settings")
    now = datetime.now()
    log.set_date_time(now)
    log.set_user_id("admin")
    log.set_interface_type("control_panel")

    assert log.get_event_id() == 10
    assert log.get_event_type() == "CHANGE"
    assert log.get_description() == "Updated settings"
    assert log.get_date_time() == now
    assert log.get_user_id() == "admin"
    assert log.get_interface_type() == "control_panel"
