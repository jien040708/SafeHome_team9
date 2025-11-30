"""
Test runner script for all alarm-related tests.

This script runs all alarm-related tests and generates coverage reports.
"""

import sys
import subprocess
from pathlib import Path

def run_tests_with_coverage():
    """Run all alarm-related tests with coverage report."""
    
    test_files = [
        "tests/security/test_alarm_class.py",
        "tests/security/test_alarm_integration.py",
        "tests/security/test_alarm_clear.py",
        "tests/security/test_sensor_trigger_alarm.py",
        "tests/domain/test_system_controller_alarm.py",
        "security/test_security_system.py",  # Existing tests with alarm additions
    ]
    
    # Check which files exist
    existing_files = []
    for test_file in test_files:
        if Path(test_file).exists():
            existing_files.append(test_file)
        else:
            print(f"Warning: {test_file} not found, skipping...")
    
    if not existing_files:
        print("No test files found!")
        return False
    
    # Run pytest with coverage
    cmd = [
        "pytest",
        "-v",
        "--cov=security.security_system",
        "--cov=domain.system_controller",
        "--cov=domain.system",
        "--cov-report=term-missing",
        "--cov-report=html",
    ] + existing_files
    
    print(f"Running tests: {', '.join(existing_files)}")
    print(f"Command: {' '.join(cmd)}")
    
    result = subprocess.run(cmd)
    
    return result.returncode == 0


if __name__ == "__main__":
    success = run_tests_with_coverage()
    sys.exit(0 if success else 1)

