"""
Test script for Configure System Settings feature
Tests the API endpoints and validation logic
"""
import requests
import json

BASE_URL = "http://localhost:5000"

# First, we need to login to get a session
def login():
    """Login to get authenticated session"""
    session = requests.Session()

    print("=" * 60)
    print("Step 1: Logging in...")
    print("=" * 60)

    # First password validation
    response = session.post(f"{BASE_URL}/api/login/first", json={
        "username": "admin",
        "password": "1234"
    })

    if response.status_code == 200:
        print("[OK] First password validated")
    else:
        print(f"[FAIL] First password failed: {response.json()}")
        return None

    # Second password validation (admin user doesn't have second password by default)
    # We'll create a web user for testing
    return session

def test_get_settings(session):
    """Test GET /api/settings endpoint"""
    print("\n" + "=" * 60)
    print("Step 2: Testing GET /api/settings")
    print("=" * 60)

    response = session.get(f"{BASE_URL}/api/settings")

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("[OK] Successfully retrieved settings:")
            settings = data['settings']
            print(f"  - Monitoring Phone: {settings['monitoring_service_phone']}")
            print(f"  - Homeowner Phone: {settings['homeowner_phone']}")
            print(f"  - Lock Time: {settings['system_lock_time']}s")
            print(f"  - Alarm Delay: {settings['alarm_delay_time']}s")
            return settings
        else:
            print(f"[FAIL] Failed: {data.get('message')}")
    else:
        print(f"[FAIL] HTTP {response.status_code}: {response.text}")

    return None

def test_update_settings_valid(session):
    """Test PUT /api/settings with valid data"""
    print("\n" + "=" * 60)
    print("Step 3: Testing PUT /api/settings (Valid Data)")
    print("=" * 60)

    new_settings = {
        "monitoring_service_phone": "111-222-3333",
        "homeowner_phone": "444-555-6666",
        "system_lock_time": 45,
        "alarm_delay_time": 90
    }

    print("Updating settings to:")
    print(f"  - Monitoring Phone: {new_settings['monitoring_service_phone']}")
    print(f"  - Homeowner Phone: {new_settings['homeowner_phone']}")
    print(f"  - Lock Time: {new_settings['system_lock_time']}s")
    print(f"  - Alarm Delay: {new_settings['alarm_delay_time']}s")

    response = session.put(
        f"{BASE_URL}/api/settings",
        json=new_settings,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("[OK] Settings updated successfully!")
            return True
        else:
            print(f"[FAIL] Failed: {data.get('message')}")
    else:
        print(f"[FAIL] HTTP {response.status_code}: {response.text}")

    return False

def test_update_settings_invalid_phone(session):
    """Test PUT /api/settings with invalid phone format"""
    print("\n" + "=" * 60)
    print("Step 4: Testing PUT /api/settings (Invalid Phone)")
    print("=" * 60)

    invalid_settings = {
        "monitoring_service_phone": "111-22-3333",  # Invalid format
        "homeowner_phone": "444-555-6666",
        "system_lock_time": 30,
        "alarm_delay_time": 60
    }

    print("Attempting to update with invalid phone: 111-22-3333")

    response = session.put(
        f"{BASE_URL}/api/settings",
        json=invalid_settings,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 400:
        data = response.json()
        if not data.get('success') and data.get('errors'):
            print("[OK] Validation correctly rejected invalid phone:")
            for error in data['errors']:
                print(f"  - {error}")
            return True
        else:
            print("[FAIL] Response format unexpected")
    else:
        print(f"[FAIL] Expected HTTP 400, got {response.status_code}")

    return False

def test_update_settings_invalid_time(session):
    """Test PUT /api/settings with invalid time values"""
    print("\n" + "=" * 60)
    print("Step 5: Testing PUT /api/settings (Invalid Time)")
    print("=" * 60)

    invalid_settings = {
        "monitoring_service_phone": "111-222-3333",
        "homeowner_phone": "444-555-6666",
        "system_lock_time": 0,  # Invalid: must be > 0
        "alarm_delay_time": -10  # Invalid: must be >= 0
    }

    print("Attempting to update with invalid times:")
    print(f"  - Lock Time: {invalid_settings['system_lock_time']} (should be > 0)")
    print(f"  - Alarm Delay: {invalid_settings['alarm_delay_time']} (should be >= 0)")

    response = session.put(
        f"{BASE_URL}/api/settings",
        json=invalid_settings,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 400:
        data = response.json()
        if not data.get('success') and data.get('errors'):
            print("[OK] Validation correctly rejected invalid times:")
            for error in data['errors']:
                print(f"  - {error}")
            return True
        else:
            print("[FAIL] Response format unexpected")
    else:
        print(f"[FAIL] Expected HTTP 400, got {response.status_code}")

    return False

def test_verify_final_settings(session):
    """Verify the final settings after all tests"""
    print("\n" + "=" * 60)
    print("Step 6: Verifying Final Settings")
    print("=" * 60)

    response = session.get(f"{BASE_URL}/api/settings")

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            settings = data['settings']
            print("[OK] Final settings in database:")
            print(f"  - Monitoring Phone: {settings['monitoring_service_phone']}")
            print(f"  - Homeowner Phone: {settings['homeowner_phone']}")
            print(f"  - Lock Time: {settings['system_lock_time']}s")
            print(f"  - Alarm Delay: {settings['alarm_delay_time']}s")
            return True

    print("[FAIL] Failed to retrieve final settings")
    return False

def main():
    print("\n" + "=" * 60)
    print("Testing Configure System Settings Feature")
    print("=" * 60)

    # Note: We need a logged-in session to test the settings API
    # For this test, we'll use requests.Session() which maintains cookies
    session = requests.Session()

    # Since we need authentication, let's create a test web user first
    print("\nNote: This test requires a logged-in web session.")
    print("Please ensure you have a web user created.")
    print("You can create one using: python create_web_user.py")
    print("\nFor automated testing, we'll try to login with admin account...")

    # Try to login as admin via control panel (if it works via web)
    # Otherwise, you'll need to manually login via the web interface

    print("\n" + "=" * 60)
    print("Starting API Tests (assuming session exists)")
    print("=" * 60)

    # Test without authentication first
    print("\nTest 1: GET /api/settings (without authentication)")
    response = session.get(f"{BASE_URL}/api/settings")
    if response.status_code == 401:
        print("[OK] Correctly rejected unauthenticated request")
    else:
        print(f"[FAIL] Expected 401, got {response.status_code}")

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print("\nManual Testing Required:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Login with your web credentials")
    print("3. Click 'Configure System Settings' button")
    print("4. Try updating the settings with valid data")
    print("5. Try updating with invalid phone format (e.g., 111-22-3333)")
    print("6. Try updating with invalid times (e.g., lock_time=0)")
    print("\nExpected Results:")
    print("- Valid data should update successfully")
    print("- Invalid phone should show error message")
    print("- Invalid times should show error message")
    print("- All changes should be saved to the database")

if __name__ == "__main__":
    main()
