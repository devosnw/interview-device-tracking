import pytest

from idt.domains import (
    Device,
    Dimmer,
    Lock,
    LockState,
    Switch,
    SwitchState,
    Thermostat,
    Hub,
    Dwelling,
)


def hub() -> Hub:
    return Hub(id="id", devices=[], dwelling=None)


class TestDevice:
    @pytest.mark.parametrize("hub", [None, hub()])
    @pytest.mark.parametrize("id_", [None, "id"])
    def test_init(self, id_, hub):
        device = Device(id=id_, hub=hub)

        assert device.id == id_
        assert device.hub == hub


class TestSwitch:
    @pytest.mark.parametrize("state", [ss for ss in SwitchState])
    def test_init(self, state):
        switch = Switch(state=state)

        assert switch.state == state


class TestDimmer:
    @pytest.mark.parametrize("brightness", [0, 50, 100])
    def test_init(self, brightness):
        dimmer = Dimmer(brightness=brightness)

        dimmer.brightness == brightness


class TestLock:
    @pytest.mark.parametrize("code", [[], ["1", "2", "3"]])
    @pytest.mark.parametrize("state", [ls for ls in LockState])
    def test_init(self, state, code):
        lock = Lock(state=state, code=code)

        lock.state == state
        lock.code == code


class TestThermostat:
    @pytest.mark.parametrize("actual_temp_f", [-100.0, 0.0, 50.0, 100.0, 200.0])
    @pytest.mark.parametrize("target_temp_f", [50.0, 75.0, 100.0])
    def test_init(self, target_temp_f, actual_temp_f):
        thermostat = Thermostat(
            target_temp_f=target_temp_f, actual_temp_f=actual_temp_f
        )

        thermostat.target_temp_f = target_temp_f
        thermostat.actual_temp_f = actual_temp_f


class TestHub:
    @pytest.mark.parametrize("dwelling", [None, Dwelling()])
    @pytest.mark.parametrize("devices", [[], [Switch(), Lock()]])
    @pytest.mark.parametrize("id_", [None, "id"])
    def test_init(self, id_, devices, dwelling):
        hub = Hub(id=id_, devices=devices, dwelling=dwelling)

        assert hub.id == id_
        assert hub.devices == devices
        assert hub.dwelling == dwelling

        for device in hub.devices:
            assert device.hub == hub


class TestDwelling:
    @pytest.mark.parametrize("hubs", [[], [Hub(id="1"), Hub(id="2")]])
    @pytest.mark.parametrize("id_", [None, "id"])
    def test_init(self, id_, hubs):
        dwelling = Dwelling(id=id_, hubs=hubs)

        assert dwelling.id == id_
        assert dwelling.hubs == hubs

        for hub in dwelling.hubs:
            assert hub.dwelling == dwelling
