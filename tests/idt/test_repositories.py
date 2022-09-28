from idt.repositories import DeviceRepository


class TestDeviceRepository:
    def test_init(self):
        assert DeviceRepository() is not None
