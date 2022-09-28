import pytest
from pytest_mock import MockerFixture

from idt.domains.devices import Device
from idt.repositories import DeviceRepository


@pytest.fixture
def device_repository() -> DeviceRepository:
    return DeviceRepository()


@pytest.fixture
def device() -> Device:
    return Device()


class TestDeviceRepository:
    def test_init(self):
        assert DeviceRepository() is not None

    class TestCreate:
        def test_existing(self, device_repository: DeviceRepository, device: Device):
            device.id = "exists"

            with pytest.raises(ValueError) as e:
                device_repository.create(device)

            assert str(e.value) == "Device exists id=exists"

        def test_success(
            self,
            mocker: MockerFixture,
            device_repository: DeviceRepository,
            device: Device,
        ):
            mocker.patch("idt.repositories.uuid.uuid4", return_value="def-a-uuid")
            devices = mocker.patch.dict("idt.repositories._DEVICES")

            device = device_repository.create(device)

            assert device.id == "def-a-uuid"
            assert devices == {"def-a-uuid": device}
