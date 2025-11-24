from __future__ import annotations

from typing import Iterable, List


class ModesViewModel:
    """View-model that encapsulates security mode interactions."""

    def __init__(self, system):
        self.system = system

    @property
    def controller(self):
        return getattr(self.system, "system_controller", None)

    @property
    def config_manager(self):
        return getattr(self.system, "configuration_manager", None)

    def change_mode(self, mode: str) -> tuple[bool, str | None]:
        controller = self.controller
        if not controller:
            return False, "System is not running."
        try:
            success = controller.set_security_mode(mode)
        except Exception as exc:
            return False, str(exc)
        return bool(success), None

    def resolve_zone_names(self, armed_zones: Iterable[int] | None) -> List[str]:
        if not armed_zones:
            return []
        config = self.config_manager
        if config:
            zone_map = config.get_zone_name_map()
            return [zone_map.get(str(zone), str(zone)) for zone in sorted(armed_zones)]
        return [str(zone) for zone in sorted(armed_zones)]
