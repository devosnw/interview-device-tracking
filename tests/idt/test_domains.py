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
    def test_init(self, hub):
        device = Device(id="id", hub=hub)

        assert device.id == "id"
        assert device.hub == hub


class TestSwitch:
    @pytest.mark.parametrize("state", [ss for ss in SwitchState])
    @pytest.mark.parametrize("hub", [None, hub()])
    def test_init(self, hub, state):
        switch = Switch(id="id", hub=hub, state=state)

        assert switch.state == state


class TestDimmer:
    @pytest.mark.parametrize("brightness", [0, 50, 100])
    @pytest.mark.parametrize("hub", [None, hub()])
    def test_init(self, hub, brightness):
        dimmer = Dimmer(id="id", hub=hub, brightness=brightness)

        dimmer.brightness == brightness


class TestLock:
    @pytest.mark.parametrize("code", [[], ["1", "2", "3"]])
    @pytest.mark.parametrize("state", [ls for ls in LockState])
    @pytest.mark.parametrize("hub", [None, hub()])
    def test_init(self, hub, state, code):
        lock = Lock(id="id", hub=hub, state=state, code=code)

        lock.state == state
        lock.code == code


class TestThermostat:
    @pytest.mark.parametrize("actual_temp_f", [])
    @pytest.mark.parametrize("target_temp_f", [])
    @pytest.mark.parametrize("hub", [None, hub()])
    def test_init(self, hub, target_temp_f, actual_temp_f):
        thermostat = Thermostat(
            id="id", hub=hub, target_temp_f=target_temp_f, actual_temp_f=actual_temp_f
        )

        thermostat.target_temp_f = target_temp_f
        thermostat.actual_temp_f = actual_temp_f


class TestHub:
    @pytest.mark.parametrize(
        "devices",
        [
            [],
            [
                Switch(
                    id="id",
                    hub=None,
                    state=SwitchState.OFF,
                ),
                Dimmer(
                    id="id",
                    hub=None,
                    brightness=0,
                ),
            ],
        ],
    )
    def test_init(self, devices):
        hub = Hub(id="id", devices=devices, dwelling=None)

        assert hub.devices == devices

        for device in hub.devices:
            assert device.hub == hub


class TestDwelling:
    @pytest.mark.parametrize(
        "hubs",
        [
            [],
            [
                Hub(id="1", devices=[], dwelling=None),
                Hub(id="2", devices=[], dwelling=None),
            ],
        ],
    )
    def test_init(self, hubs):
        dwelling = Dwelling(id="id", hubs=hubs)

        assert dwelling.hubs == hubs

        for hub in dwelling.hubs:
            assert hub.dwelling == dwelling
