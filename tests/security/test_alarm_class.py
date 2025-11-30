"""
Test cases for Alarm class functionality.

Tests cover:
- Alarm initialization
- Alarm ID management
- Alarm location management
- Alarm ringing status
- Alarm ring/silence functionality
"""

from __future__ import annotations

import sys
from io import StringIO
from unittest.mock import patch

from security.security_system import Alarm


def test_alarm_initialization_default():
    """Test Alarm initialization with default parameters."""
    alarm = Alarm()
    assert alarm.get_id() == 0
    assert alarm.get_location() == (0, 0)
    assert alarm.is_ringing() is False


def test_alarm_initialization_custom():
    """Test Alarm initialization with custom parameters."""
    alarm = Alarm(alarm_id=1, x_coord=100, y_coord=200)
    assert alarm.get_id() == 1
    assert alarm.get_location() == (100, 200)
    assert alarm.is_ringing() is False


def test_alarm_set_id_valid():
    """Test setting alarm ID with valid value."""
    alarm = Alarm()
    result = alarm.set_id(5)
    assert result is True
    assert alarm.get_id() == 5


def test_alarm_set_id_invalid():
    """Test setting alarm ID with invalid (negative) value."""
    alarm = Alarm(alarm_id=10)
    result = alarm.set_id(-1)
    assert result is False
    assert alarm.get_id() == 10  # Should remain unchanged


def test_alarm_get_location():
    """Test getting alarm location."""
    alarm = Alarm(alarm_id=2, x_coord=150, y_coord=250)
    location = alarm.get_location()
    assert location == (150, 250)
    assert isinstance(location, tuple)


def test_alarm_is_ringing_false():
    """Test is_ringing() returns False when alarm is not ringing."""
    alarm = Alarm()
    assert alarm.is_ringing() is False


def test_alarm_is_ringing_true():
    """Test is_ringing() returns True when alarm is ringing."""
    alarm = Alarm()
    alarm.ring_alarm(True)
    assert alarm.is_ringing() is True


def test_alarm_ring_alarm_activate():
    """Test ring_alarm(True) activates the alarm and prints message."""
    alarm = Alarm(alarm_id=3, x_coord=300, y_coord=400)
    
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    alarm.ring_alarm(True)
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    output = captured_output.getvalue()
    assert alarm.is_ringing() is True
    assert "RINGING" in output
    assert "Alarm 3" in output
    assert "(300, 400)" in output


def test_alarm_ring_alarm_silence():
    """Test ring_alarm(False) silences the alarm and prints message."""
    alarm = Alarm(alarm_id=4, x_coord=500, y_coord=600)
    
    # First activate the alarm
    alarm.ring_alarm(True)
    assert alarm.is_ringing() is True
    
    # Capture stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    
    alarm.ring_alarm(False)
    
    # Restore stdout
    sys.stdout = sys.__stdout__
    
    output = captured_output.getvalue()
    assert alarm.is_ringing() is False
    assert "silenced" in output
    assert "Alarm 4" in output
    assert "(500, 600)" in output


def test_alarm_ring_alarm_multiple_calls():
    """Test multiple calls to ring_alarm maintain correct state."""
    alarm = Alarm()
    
    alarm.ring_alarm(True)
    assert alarm.is_ringing() is True
    
    alarm.ring_alarm(True)  # Ring again while already ringing
    assert alarm.is_ringing() is True
    
    alarm.ring_alarm(False)
    assert alarm.is_ringing() is False
    
    alarm.ring_alarm(False)  # Silence again while already silent
    assert alarm.is_ringing() is False


def test_alarm_state_consistency():
    """Test that alarm state is consistent across all methods."""
    alarm = Alarm(alarm_id=10, x_coord=1000, y_coord=2000)
    
    # Initially not ringing
    assert alarm.is_ringing() is False
    
    # After ringing
    alarm.ring_alarm(True)
    assert alarm.is_ringing() is True
    assert alarm._status is True
    
    # After silencing
    alarm.ring_alarm(False)
    assert alarm.is_ringing() is False
    assert alarm._status is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

