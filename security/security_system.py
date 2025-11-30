# safehome/security/security_system.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Callable, Dict, Iterable, List, Optional, Set, TYPE_CHECKING

from .events import SensorEvent, SensorStatus, SensorType


class Alarm:
    """
    Alarm class as defined in the UML diagram.
    Represents an alarm device with location and status.
    """
    
    def __init__(self, alarm_id: int = 0, x_coord: int = 0, y_coord: int = 0):
        self._id: int = alarm_id
        self._x_coord: int = x_coord
        self._y_coord: int = y_coord
        self._status: bool = False  # False = not ringing, True = ringing
    
    def set_id(self, alarm_id: int) -> bool:
        """Set the alarm ID."""
        if alarm_id < 0:
            return False
        self._id = alarm_id
        return True
    
    def get_id(self) -> int:
        """Get the alarm ID."""
        return self._id
    
    def get_location(self) -> tuple[int, int]:
        """Get the alarm location as (x, y) coordinates."""
        return (self._x_coord, self._y_coord)
    
    def is_ringing(self) -> bool:
        """Check if the alarm is currently ringing."""
        return self._status
    
    def ring_alarm(self, status_value: bool) -> None:
        """
        Ring or silence the alarm.
        Args:
            status_value: True to ring the alarm, False to silence it.
        """
        self._status = status_value
        
        if status_value:
            # Alarm is ringing
            print(f"🚨 [ALARM] Alarm {self._id} at ({self._x_coord}, {self._y_coord}) is RINGING! 🚨")
            import sys
            sys.stdout.write(f"🚨 [ALARM] Alarm {self._id} at ({self._x_coord}, {self._y_coord}) is RINGING! 🚨\n")
            sys.stdout.flush()
        else:
            # Alarm is silenced
            print(f"[ALARM] Alarm {self._id} at ({self._x_coord}, {self._y_coord}) is silenced.")
            import sys
            sys.stdout.write(f"[ALARM] Alarm {self._id} at ({self._x_coord}, {self._y_coord}) is silenced.\n")
            sys.stdout.flush()


class SecurityMode(Enum):
    """High-level security modes defined in the SRS."""

    DISARMED = auto()
    HOME = auto()
    AWAY = auto()
    STAY = auto()  # aka OVERNIGHT
    EXTENDED_TRAVEL = auto()


class AlarmState(Enum):
    """Lifecycle state for the alarm subsystem."""

    IDLE = auto()
    ENTRY_DELAY = auto()
    ALARM_ACTIVE = auto()


@dataclass
class IntrusionRecord:
    """Domain log entry for UC2 events."""

    timestamp: datetime
    sensor_id: Optional[str]
    zone_id: Optional[str]
    sensor_type: Optional[SensorType]
    mode: SecurityMode
    action: str
    status: Optional[SensorStatus]
    details: Optional[str] = None


if TYPE_CHECKING:  # pragma: no cover
    from .interfaces import CameraGateway, SecurityEventListener, SecurityStatus


class SecuritySystem:
    """
    Domain service for Use Case 2 (Security).

    This class owns the business rules for arming/disarming, safety zones,
    entry-delay handling, panic behavior, siren/monitoring triggers, and
    intrusion logging. UI concerns, authentication, and concrete devices
    must be provided through the injected callbacks/interfaces.
    """

    def __init__(
        self,
        *,
        get_delay_time: Callable[[], timedelta],
        call_monitoring_service: Callable[[str], None],
        activate_siren: Callable[[], None],
        deactivate_siren: Callable[[], None],
        get_monitored_sensors_state: Callable[[], Dict[str, SensorStatus]],
        event_listener: Optional[SecurityEventListener] = None,
        camera_gateway: Optional[CameraGateway] = None,
    ) -> None:
        self._mode: SecurityMode = SecurityMode.DISARMED
        self._alarm_state: AlarmState = AlarmState.IDLE
        self._armed_zones: Set[str] = set()
        self._zone_sensors: Dict[str, Set[str]] = {}
        self._sensor_zones: Dict[str, str] = {}
        self._sensor_types: Dict[str, SensorType] = {}
        self._delay_deadline: Optional[datetime] = None
        self._monitoring_call_scheduled = False
        self._last_trigger_event: Optional[SensorEvent] = None
        self._alarm_started_at: Optional[datetime] = None
        self._monitoring_deadline: Optional[datetime] = None

        self._get_delay_time = get_delay_time
        self._call_monitoring_service = call_monitoring_service
        self._activate_siren = activate_siren
        self._deactivate_siren = deactivate_siren
        self._get_monitored_sensors_state = get_monitored_sensors_state
        self._listener: Optional["SecurityEventListener"] = event_listener
        self._camera_gateway: Optional["CameraGateway"] = camera_gateway

        self._intrusion_logs: List[IntrusionRecord] = []

    # ------------------------------------------------------------------
    # Configuration APIs
    # ------------------------------------------------------------------

    def register_sensor(
        self,
        sensor_id: str,
        sensor_type: SensorType,
        zone_id: Optional[str] = None,
    ) -> None:
        """Register a sensor so the system knows its type and zone."""
        self._sensor_types[sensor_id] = sensor_type
        if zone_id:
            self.assign_sensor_to_zone(sensor_id, zone_id)

    def assign_sensor_to_zone(self, sensor_id: str, zone_id: str) -> None:
        """Associate an existing sensor with a zone."""
        self._sensor_zones[sensor_id] = zone_id
        self._zone_sensors.setdefault(zone_id, set()).add(sensor_id)

    def unassign_sensor(self, sensor_id: str) -> None:
        """Remove a sensor from any zone tracking."""
        zone_id = self._sensor_zones.pop(sensor_id, None)
        if zone_id:
            sensors = self._zone_sensors.get(zone_id)
            if sensors:
                sensors.discard(sensor_id)
                if not sensors:
                    self._zone_sensors.pop(zone_id, None)
        self._notify_status_change()

    def remove_zone(self, zone_id: str) -> None:
        """Remove a zone definition."""
        sensors = self._zone_sensors.pop(zone_id, set())
        for sensor in sensors:
            self._sensor_zones.pop(sensor, None)
        self._armed_zones.discard(zone_id)
        self._notify_status_change()

    def set_event_listener(self, listener: Optional["SecurityEventListener"]) -> None:
        """Attach or replace the listener that receives security events."""
        self._listener = listener
        self._notify_status_change()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def mode(self) -> SecurityMode:
        return self._mode

    @property
    def alarm_state(self) -> AlarmState:
        return self._alarm_state

    def arm(self, mode: SecurityMode, zones: Optional[Set[str]] = None) -> None:
        """
        Arm the system in the given mode. Zones defaults to all known zones.
        Preconditions (auth, lock state) are enforced by UC1 before calling.
        """
        if mode is SecurityMode.DISARMED:
            raise ValueError("Use disarm() instead of arming DISARMED mode.")

        target_zones = zones or set(self._zone_sensors.keys())
        if not self._check_doors_and_windows_closed(target_zones):
            raise RuntimeError("Cannot arm: door/window sensors are open.")

        self._mode = mode
        self._armed_zones = target_zones
        self._alarm_state = AlarmState.IDLE
        self._delay_deadline = None
        self._monitoring_call_scheduled = False
        self._last_trigger_event = None
        self._log(None, f"ARMED_{mode.name}")
        self._notify_status_change()

    def disarm(self, *, cleared_by: Optional[str] = None) -> None:
        """Disarm the system and silence any active alarm."""
        self._mode = SecurityMode.DISARMED
        self._armed_zones.clear()
        self._delay_deadline = None
        self._monitoring_call_scheduled = False
        self._last_trigger_event = None

        if self._alarm_state is not AlarmState.IDLE:
            self._deactivate_siren()
            if self._listener:
                self._listener.on_alarm_cleared(cleared_by or "UNKNOWN")

        self._alarm_state = AlarmState.IDLE
        self._alarm_started_at = None
        self._monitoring_deadline = None
        self._log(None, "DISARMED", details=f"by {cleared_by}" if cleared_by else None)
        self._notify_status_change()

    def clear_alarm(self, *, cleared_by: Optional[str] = None) -> None:
        """Clear the alarm without disarming the system."""
        if self._alarm_state is AlarmState.IDLE:
            return  # No alarm to clear

        self._deactivate_siren()
        self._alarm_state = AlarmState.IDLE
        self._alarm_started_at = None
        self._monitoring_deadline = None
        self._monitoring_call_scheduled = False
        
        if self._listener:
            self._listener.on_alarm_cleared(cleared_by or "UNKNOWN")
        
        self._log(None, "ALARM_CLEARED", details=f"by {cleared_by}" if cleared_by else None)
        self._notify_status_change()

    def handle_sensor_event(self, event: SensorEvent) -> None:
        """
        Evaluate an incoming sensor event and start the entry delay/alarm cycle
        when appropriate.
        """
        print(f"[SecuritySystem] handle_sensor_event called: sensor={event.sensor_id}, type={event.sensor_type.name}, status={event.status.name}, mode={self._mode.name}")
        
        if self._mode is SecurityMode.DISARMED:
            print(f"[SecuritySystem] System is DISARMED - ignoring sensor event")
            return

        if not self._is_sensor_armed(event):
            print(f"[SecuritySystem] Sensor {event.sensor_id} is not armed - ignoring event")
            return

        now = event.timestamp
        if self._alarm_state is AlarmState.ENTRY_DELAY:
            self._log(event, "ENTRY_DELAY_RETRIGGERED")
            return

        if self._alarm_state is AlarmState.ALARM_ACTIVE:
            self._log(event, "ALARM_ALREADY_ACTIVE")
            return

        # Immediate alarm activation on sensor trigger
        self._alarm_state = AlarmState.ALARM_ACTIVE
        self._alarm_started_at = now
        self._monitoring_call_scheduled = False
        self._delay_deadline = None
        self._last_trigger_event = event
        
        # Log alarm activation
        sensor_id = event.sensor_id or "Unknown"
        print(f"🚨 [ALARM] Sensor {sensor_id} triggered - ALARM ACTIVATED! 🚨")
        import sys
        sys.stdout.write(f"🚨 [ALARM] Sensor {sensor_id} triggered - ALARM ACTIVATED! 🚨\n")
        sys.stdout.flush()
        
        # Activate siren immediately
        self._activate_siren()
        if self._camera_gateway:
            self._camera_gateway.trigger_all("INTRUSION")
        
        # Schedule monitoring service call after alarm_delay_time
        delay_time = self._get_delay_time()
        self._monitoring_deadline = now + delay_time
        
        self._log(event, "ALARM_TRIGGERED")
        if self._listener:
            self._listener.on_alarm_activated(event)
        self._notify_status_change()

    def tick(self, now: datetime) -> None:
        """
        Periodic driver (e.g., called every second). 
        - If an entry delay expired, escalate to full alarm.
        - If alarm is active and alarm_delay_time passed, notify monitoring service.
        """
        # Handle entry delay expiration
        if (
            self._alarm_state is AlarmState.ENTRY_DELAY
            and self._delay_deadline is not None
            and now >= self._delay_deadline
        ):
            trigger = self._last_trigger_event
            sensor_id = trigger.sensor_id if trigger else "Unknown"
            
            print(f"[SecuritySystem] Entry delay expired - ALARM ACTIVATED for sensor {sensor_id}!")
            import sys
            sys.stdout.write(f"[SecuritySystem] Entry delay expired - ALARM ACTIVATED for sensor {sensor_id}!\n")
            sys.stdout.flush()
            
            self._alarm_state = AlarmState.ALARM_ACTIVE
            self._alarm_started_at = now
            self._monitoring_call_scheduled = False
            self._activate_siren()
            if self._camera_gateway:
                self._camera_gateway.trigger_all("INTRUSION")
            # Schedule monitoring service call after alarm_delay_time
            delay_time = self._get_delay_time()
            self._monitoring_deadline = now + delay_time
            self._log(trigger, "ALARM_TRIGGERED")
            if self._listener:
                self._listener.on_alarm_activated(trigger)
            self._notify_status_change()
        
        # Handle monitoring service call after alarm_delay_time
        if (
            self._alarm_state is AlarmState.ALARM_ACTIVE
            and self._monitoring_deadline is not None
            and not self._monitoring_call_scheduled
            and now >= self._monitoring_deadline
        ):
            # Get current condition information
            sensor_states = self._get_monitored_sensors_state()
            condition_info = f"Alarm active. Sensor states: {sensor_states}"
            
            self._call_monitoring_service(condition_info)
            self._monitoring_call_scheduled = True
            
            print(f"[SecuritySystem] Monitoring service notified with condition information: {condition_info}")
            import sys
            sys.stdout.write(f"[SecuritySystem] Monitoring service notified with condition information: {condition_info}\n")
            sys.stdout.flush()

    def trigger_panic(self) -> None:
        """Immediate alarm regardless of armed mode. Monitoring call scheduled after delay."""
        self._alarm_state = AlarmState.ALARM_ACTIVE
        self._alarm_started_at = datetime.utcnow()
        self._delay_deadline = None
        self._monitoring_call_scheduled = False
        
        # Log panic alarm activation
        print(f"🚨 [PANIC ALARM] PANIC button pressed - ALARM ACTIVATED! 🚨")
        import sys
        sys.stdout.write(f"🚨 [PANIC ALARM] PANIC button pressed - ALARM ACTIVATED! 🚨\n")
        sys.stdout.flush()
        
        self._activate_siren()
        if self._camera_gateway:
            self._camera_gateway.trigger_all("PANIC")
        # Schedule monitoring service call after alarm_delay_time
        delay_time = self._get_delay_time()
        self._monitoring_deadline = self._alarm_started_at + delay_time
        self._log(None, "PANIC_TRIGGERED")
        if self._listener:
            self._listener.on_alarm_activated(None)
        self._notify_status_change()

    def get_intrusion_logs(self) -> List[IntrusionRecord]:
        """Return a copy of the intrusion log."""
        return list(self._intrusion_logs)

    def get_status(self) -> Optional["SecurityStatus"]:
        """
        Produce a SecurityStatus DTO for UI/REST layers. Returns None when
        the interfaces module is unavailable (e.g., during lightweight tests).
        """
        try:
            from .interfaces import SecurityStatus  # local import avoids circular dependency
        except Exception:  # pragma: no cover
            return None

        return SecurityStatus(
            mode=self._mode,
            alarm_state=self._alarm_state,
            armed_zones=set(self._armed_zones),
            entry_delay_deadline=self._delay_deadline,
            monitoring_call_scheduled=self._monitoring_call_scheduled,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_zone(self, event: SensorEvent) -> Optional[str]:
        if event.zone_id:
            return event.zone_id
        return self._sensor_zones.get(event.sensor_id)

    def _check_doors_and_windows_closed(self, zones: Set[str]) -> bool:
        """
        Verify perimeter sensors (door/window) in the target zones are closed
        before arming.
        """
        if not zones:
            # No zones defined -> check every known door/window sensor.
            sensors_to_check: Iterable[str] = [
                sid
                for sid, stype in self._sensor_types.items()
                if stype in (SensorType.DOOR, SensorType.WINDOW)
            ]
        else:
            sensors_to_check = set()
            for zone in zones:
                sensors_to_check |= self._zone_sensors.get(zone, set())

        states = self._get_monitored_sensors_state()
        for sensor_id in sensors_to_check:
            stype = self._sensor_types.get(sensor_id)
            if stype not in (SensorType.DOOR, SensorType.WINDOW):
                continue
            status = states.get(sensor_id)
            if status is SensorStatus.OPEN:
                return False
        return True

    def _is_sensor_armed(self, event: SensorEvent) -> bool:
        """Determine if a sensor should trigger alarms for the current mode."""
        zone_id = self._resolve_zone(event)
        if self._armed_zones and zone_id and zone_id not in self._armed_zones:
            return False

        if self._mode in {SecurityMode.HOME, SecurityMode.STAY}:
            return event.sensor_type in (SensorType.DOOR, SensorType.WINDOW)

        # AWAY / EXTENDED_TRAVEL: all sensors within armed zones are active.
        if self._mode in {SecurityMode.AWAY, SecurityMode.EXTENDED_TRAVEL}:
            return True

        return False

    def _log(
        self,
        event: Optional[SensorEvent],
        action: str,
        *,
        details: Optional[str] = None,
    ) -> None:
        record = IntrusionRecord(
            timestamp=event.timestamp if event else datetime.utcnow(),
            sensor_id=event.sensor_id if event else None,
            zone_id=self._resolve_zone(event) if event else None,
            sensor_type=event.sensor_type if event else None,
            mode=self._mode,
            action=action,
            status=event.status if event else None,
            details=details,
        )
        self._intrusion_logs.append(record)
        if self._listener:
            self._listener.on_intrusion_logged(record)

    def _notify_status_change(self) -> None:
        if self._listener:
            status = self.get_status()
            if status:
                self._listener.on_status_changed(status)
