from idt.domains import Device, Dimmer, Lock, Switch, Thermostat, Hub, Dwelling


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


class TestHub:
    class TestInit:
        def test_defaults(self):
            hub = Hub()

            assert hub.devices == []

        def test_fields(self):
            devices = [Switch(), Dimmer()]

            hub = Hub(devices=devices)

            assert hub.devices == devices


class TestDwelling:
    class TestInit:
        def test_defaults(self):
            dwelling = Dwelling()

            assert dwelling.hubs == []

        def test_fields(self):
            hubs = [Hub(), Hub()]

            dwelling = Dwelling(hubs=hubs)

            assert dwelling.hubs == hubs
