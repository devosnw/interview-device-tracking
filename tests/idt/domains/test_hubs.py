from idt.domains.devices import Dimmer, Switch
from idt.domains.hubs import Hub


class TestHub:
    class TestInit:
        def test_defaults(self):
            hub = Hub()

            assert hub.devices == []

        def test_fields(self):
            devices = [Switch(), Dimmer()]

            hub = Hub(devices=devices)

            assert hub.devices == devices
