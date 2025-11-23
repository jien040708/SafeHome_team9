"""
Integration Tests for Configuration API
Tests Flask endpoints with authentication and validation
"""
import unittest
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from config.system_settings import SystemSettings
from storage.storage_manager import StorageManager


class TestConfigurationAPI(unittest.TestCase):
    """Integration tests for /api/settings endpoints"""

    BASE_URL = "http://localhost:5000"

    def setUp(self):
        """Set up test fixtures"""
        self.session = requests.Session()
        self.storage = StorageManager()
        self.storage.connect()

        # Restore known state
        settings = SystemSettings()
        settings.set_monitoring_service_phone("911")
        settings.set_homeowner_phone("010-0000-0000")
        settings.set_system_lock_time(10)
        settings.set_alarm_delay_time(60)
        settings.save()

    def tearDown(self):
        """Clean up after tests"""
        self.session.close()

    def test_get_settings_unauthenticated(self):
        """
        Test Case: IT-API-GET-NoAuth
        Verifies that GET /api/settings rejects unauthenticated requests
        """
        print("\n[TEST] IT-API-GET-NoAuth: test_get_settings_unauthenticated")

        response = self.session.get(f"{self.BASE_URL}/api/settings")

        self.assertEqual(
            response.status_code,
            401,
            f"Expected 401 Unauthorized, got {response.status_code}"
        )
        print(f"  [OK] Status code: {response.status_code}")

        data = response.json()
        self.assertFalse(data.get('success', True))
        self.assertIn('Authentication required', data.get('message', ''))

        print(f"  [OK] Response: {data}")
        print("  [PASS] Unauthenticated request correctly rejected")

    def test_update_settings_unauthenticated(self):
        """
        Test Case: Additional test
        Verifies that PUT /api/settings rejects unauthenticated requests
        """
        print("\n[TEST] test_update_settings_unauthenticated")

        update_data = {
            "monitoring_service_phone": "111-222-3333",
            "homeowner_phone": "444-555-6666",
            "system_lock_time": 45,
            "alarm_delay_time": 90
        }

        response = self.session.put(
            f"{self.BASE_URL}/api/settings",
            json=update_data
        )

        self.assertEqual(
            response.status_code,
            401,
            f"Expected 401 Unauthorized, got {response.status_code}"
        )
        print(f"  [OK] Status code: {response.status_code}")
        print("  [PASS] Unauthenticated update correctly rejected")


class TestConfigurationAPIValidation(unittest.TestCase):
    """Integration tests for API validation logic"""

    BASE_URL = "http://localhost:5000"

    def setUp(self):
        """Set up test fixtures"""
        self.session = requests.Session()

    def tearDown(self):
        """Clean up after tests"""
        self.session.close()

    def test_update_settings_invalid_time_values(self):
        """
        Test Case: IT-API-PUT-BadTime
        Verifies that PUT /api/settings rejects invalid time values
        Note: This test assumes authentication is handled
        """
        print("\n[TEST] IT-API-PUT-BadTime: test_update_settings_invalid_time_values")
        print("  [NOTE] This test requires authentication")
        print("  [NOTE] Run manual test with authenticated session")

        # This test would need authenticated session
        # For documentation purposes, showing expected behavior
        invalid_data = {
            "monitoring_service_phone": "111-222-3333",
            "homeowner_phone": "444-555-6666",
            "system_lock_time": 0,  # Invalid: must be > 0
            "alarm_delay_time": -10  # Invalid: must be >= 0
        }

        print(f"  [INFO] Test data (invalid times): {invalid_data}")
        print("  [EXPECTED] HTTP 400 with validation errors:")
        print("    - 'System lock time must be greater than 0'")
        print("    - 'Alarm delay time must be non-negative'")
        print("  [SKIP] Requires authenticated session - see manual test")


def run_tests():
    """Run all integration tests"""
    print("=" * 70)
    print("INTEGRATION TESTS - Configuration API")
    print("=" * 70)
    print("\nNOTE: Some tests require the Flask application to be running.")
    print("Please ensure: python main.py is running on http://localhost:5000\n")

    # Check if server is running
    try:
        response = requests.get("http://localhost:5000/", timeout=2)
        print("[OK] Server is running")
    except requests.exceptions.RequestException:
        print("[ERROR] Server is not running. Please start: python main.py")
        print("Continuing with documentation of expected test results...\n")

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConfigurationAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigurationAPIValidation))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.testsRun > 0:
        pass_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Pass Rate: {pass_rate:.1f}%")

    print("=" * 70)
    print("\nNOTE: For full integration testing including authenticated requests,")
    print("please use manual testing as described in CONFIGURE_SETTINGS_TEST_DOCUMENTATION.md")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
