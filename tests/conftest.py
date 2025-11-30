import pytest

import main as main_app
from domain.system import System
from domain.services.bootstrap_service import SystemBootstrapper
from storage.storage_manager import StorageManager


@pytest.fixture(autouse=True)
def reset_admin_account():
    """각 테스트 전에 admin 계정의 잠금 상태를 초기화합니다."""
    storage = StorageManager()
    storage.connect()
    # admin 계정 잠금 해제 및 실패 시도 초기화
    try:
        storage.execute_update(
            "UPDATE users SET is_locked = 0, failed_attempts = 0, locked_at = NULL WHERE user_id = 'admin'",
            ()
        )
        storage.execute_update(
            "UPDATE users SET is_locked = 0, failed_attempts = 0, locked_at = NULL WHERE user_id = 'homeowner'",
            ()
        )
    except Exception:
        pass  # 테이블이 없을 수 있음
    yield
    # 테스트 후에도 정리 - 먼저 연결 복원
    storage = StorageManager()
    storage.connect()  # 항상 실제 DB에 연결 복원
    try:
        storage.execute_update(
            "UPDATE users SET is_locked = 0, failed_attempts = 0, locked_at = NULL WHERE user_id = 'admin'",
            ()
        )
        storage.execute_update(
            "UPDATE users SET is_locked = 0, failed_attempts = 0, locked_at = NULL WHERE user_id = 'homeowner'",
            ()
        )
    except Exception:
        pass


@pytest.fixture(scope="session")
def safehome_system_instance():
    """Spin up the SafeHome System once for API/UI tests."""
    system = System()

    # Initialize bootstrap service to load sensors
    ui_sensors = []
    bootstrapper = SystemBootstrapper()
    bootstrapper.attach_post_turn_on_hook(system, ui_sensors)

    assert system.turn_on(), "Failed to initialize SafeHome system for tests"
    main_app.safehome_system = system
    try:
        yield system
    finally:
        system.turn_off()
        main_app.safehome_system = None


@pytest.fixture(scope="session")
def flask_app(safehome_system_instance):
    """Expose the Flask app configured for testing."""
    app = main_app.app
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(flask_app):
    """Provide an unauthenticated Flask test client."""
    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            yield test_client


@pytest.fixture
def auth_client(client):
    """Return a client with an authenticated session (web login)."""
    with client.session_transaction() as session:
        session["logged_in"] = True
        session["username"] = "admin"
    return client
