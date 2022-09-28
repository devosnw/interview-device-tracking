from idt.domains.devices import Device, Dimmer, Lock, Switch, Thermostat


class TestDevice:
    def test_init(self):
        assert Device() is not None


class TestSwitch:
    def test_init(self):
        assert Switch() is not None


class TestDimmer:
    def test_init(self):
        assert Dimmer() is not None


class TestLock:
    def test_init(self):
        assert Lock() is not None


class TestThermostat:
    def test_init(self):
        assert Thermostat() is not None
