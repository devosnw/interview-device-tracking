from idt.domains.devices import Device, Dimmer, Lock, Switch, Thermostat


class TestDevice:
    class TestInit:
        def test_defaults(self):
            device = Device()

            assert device.id is None

        def test_fields(self):
            device = Device(id="id")

            assert device.id == "id"


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
