from idt.domains.devices import Dimmer, Switch
from idt.domains.hubs import Hub


class TestHub:
    def test_init(self):
        devices = [Switch(), Dimmer()]

        hub = Hub(devices=devices)

        assert hub.devices == devices
