from typing import Mapping
import pytest
from pytest_mock import MockerFixture

from idt.domains import Device
from idt.repositories import DeviceRepository


@pytest.fixture
def device_repository() -> DeviceRepository:
    return DeviceRepository()


@pytest.fixture
def device() -> Device:
    return Device()


@pytest.fixture
def mock_devices(mocker: MockerFixture):
    return mocker.patch.dict("idt.repositories._DEVICES")


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
            mock_devices: Mapping,
        ):
            mocker.patch("idt.repositories.uuid.uuid4", return_value="def-a-uuid")

            device = device_repository.create(device)

            assert device.id == "def-a-uuid"
            assert mock_devices == {"def-a-uuid": device}

    class TestDelete:
        @pytest.mark.usefixtures("mock_devices")
        def test_not_found(self, device_repository: DeviceRepository):
            with pytest.raises(KeyError) as e:
                device_repository.delete("not-here")

            assert str(e.value) == "'not-here'"

        def test_found(
            self,
            device_repository: DeviceRepository,
            device: Device,
            mock_devices: Mapping,
        ):
            mock_devices["id"] = device

            device_repository.delete("id")

            assert mock_devices == {}

    class TestGet:
        @pytest.mark.usefixtures("mock_devices")
        def test_not_found(self, device_repository: DeviceRepository):
            with pytest.raises(KeyError) as e:
                device_repository.get("not-here")

            assert str(e.value) == "'not-here'"

        def test_found(
            self,
            device_repository: DeviceRepository,
            device: Device,
            mock_devices: Mapping,
        ):
            mock_devices["id"] = device

            assert device_repository.get("id") == device

    class TestList:
        def test_empty(self, device_repository: DeviceRepository):
            assert device_repository.list() == []

        def test_some(self, device_repository: DeviceRepository, mock_devices: Mapping):
            device_1 = Device(id="1")
            device_2 = Device(id="2")
            mock_devices[device_1.id] = device_1
            mock_devices[device_2.id] = device_2

            devices = device_repository.list()

            assert devices == [device_1, device_2]
