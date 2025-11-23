import pytest

import main as main_app
from domain.system import System


@pytest.fixture(scope="session")
def safehome_system_instance():
    """Spin up the SafeHome System once for API/UI tests."""
    system = System()
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
