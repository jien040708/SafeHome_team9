from types import SimpleNamespace

from domain.services.zones_presenter import ZonesViewModel


class StubDeviceManager:
    def __init__(self, devices):
        self.devices = devices

    def load_all_devices(self):
        return list(self.devices)


class StubConfigManager:
    def __init__(self):
        self.zones = [
            SimpleNamespace(zone_id=1, zone_name="Front Door"),
            SimpleNamespace(zone_id=2, zone_name="Back Door"),
        ]
        self.device_manager = StubDeviceManager(
            [("SensorA", "Window/Door"), ("SensorB", "Motion")]
        )
        self.assignments = {"SensorA": 1}
        self.zone_name_map = {"1": "Front Door", "2": "Back Door"}
        self.added = []
        self.renamed = []
        self.deleted = []
        self.assigned = []
        self.cleared = []

    def refresh_safety_zones(self):
        return list(self.zones)

    def add_safety_zone(self, name):
        self.added.append(name)
        return True

    def modify_safety_zone(self, zone_id, zone_name):
        self.renamed.append((zone_id, zone_name))

    def delete_safety_zone(self, zone_id):
        self.deleted.append(zone_id)

    def assign_sensor_to_zone(self, sensor_id, zone_id):
        self.assigned.append((sensor_id, zone_id))
        return True

    def remove_sensor_assignment(self, sensor_id):
        self.cleared.append(sensor_id)
        return True

    def list_sensor_assignments(self):
        return dict(self.assignments)

    def get_zone_name_map(self):
        return dict(self.zone_name_map)


class StubSystem:
    def __init__(self, config):
        self.configuration_manager = config


def make_vm():
    config = StubConfigManager()
    system = StubSystem(config)
    return ZonesViewModel(system), config


def test_get_zones_and_sensors():
    vm, _ = make_vm()
    zones = vm.get_zones()
    sensors = vm.get_sensor_ids()

    assert [z.label for z in zones] == ["[1] Front Door", "[2] Back Door"]
    assert sensors == ["SensorA", "SensorB"]


def test_assignments_map_resolves_names():
    vm, _ = make_vm()
    zone_map = vm.get_sensor_zone_map()

    assert zone_map == {"SensorA": "Front Door"}


def test_zone_mutations_forward_to_config():
    vm, config = make_vm()
    assert vm.add_zone("Garage")
    vm.rename_zone(1, "Entry")
    vm.delete_zone(2)

    assert config.added == ["Garage"]
    assert config.renamed == [(1, "Entry")]
    assert config.deleted == [2]


def test_assign_and_clear_sensor():
    vm, config = make_vm()
    assert vm.assign_sensor("SensorB", 2)
    assert vm.clear_assignment("SensorA")
    assert config.assigned == [("SensorB", 2)]
    assert config.cleared == ["SensorA"]
