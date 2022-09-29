from asyncio import locks
from typing import Mapping
import pytest
from pytest_mock import MockerFixture

from idt.domains import (
    Device,
    Dimmer,
    Hub,
    Lock,
    LockState,
    Switch,
    SwitchState,
    Thermostat,
    TypeDevice,
)
from idt.repositories import DeviceRepository, Store
from idt.usecases import DeviceUsecases


@pytest.fixture
def device_repo() -> DeviceRepository:
    return DeviceRepository(Store())


@pytest.fixture
def device_uc(device_repo: DeviceRepository) -> DeviceUsecases:
    return DeviceUsecases(device_repo)


@pytest.fixture
def device() -> Device:
    return Device()


@pytest.fixture
def mock_uuid(mocker: MockerFixture):
    return mocker.patch("idt.repositories.uuid.uuid4", return_value="a-uuid")


class TestDeviceUsecases:
    def test_init(self, device_repo):
        assert DeviceUsecases(device_repo) is not None

    class TestCreateDevice:
        def test_invalid_kwargs(self, device_uc: DeviceUsecases):
            with pytest.raises(TypeError) as e:
                device_uc.create_device(Device, {"invalid": True})

            assert (
                str(e.value)
                == "DeviceUsecases.create_device() takes 2 positional arguments but 3 were given"
            )

        @pytest.mark.usefixtures("mock_uuid")
        @pytest.mark.parametrize(
            "device_cls,kwargs,expected",
            [
                (Device, {}, Device(id="a-uuid")),
                (
                    Switch,
                    {"state": SwitchState.ON},
                    Switch(id="a-uuid", state=SwitchState.ON),
                ),
                (Dimmer, {"brightness": 40}, Dimmer(id="a-uuid", brightness=40)),
                (
                    Lock,
                    {"state": LockState.LOCKED, "code": ["1", "2", "3"]},
                    Lock(id="a-uuid", state=LockState.LOCKED, code=["1", "2", "3"]),
                ),
                (
                    Thermostat,
                    {"target_temp_f": 75.0, "actual_temp_f": 76.0},
                    Thermostat(id="a-uuid", target_temp_f=75.0, actual_temp_f=76.0),
                ),
            ],
        )
        def test_success(
            self,
            device_uc: DeviceUsecases,
            device_cls: type[TypeDevice],
            kwargs: Mapping,
            expected: TypeDevice,
        ):
            device = device_uc.create_device(device_cls, **kwargs)

            assert device == expected
            assert device_uc.repo.store.devices == {expected.id: expected}

    class TestDeleteDevice:
        def test_not_there(self, device_uc: DeviceUsecases):
            with pytest.raises(KeyError) as e:
                device_uc.delete_device("not-here")

            assert str(e.value) == "'not-here'"

        def test_success(self, device_uc: DeviceUsecases, device: Device):
            device.id = "id"
            device_uc.repo.store.devices[device.id] = device

            device_uc.delete_device("id")

            assert device_uc.repo.store.devices == {}

    class TestShowDeviceInfo:
        def test_not_there(self, device_uc: DeviceUsecases):
            with pytest.raises(KeyError) as e:
                device_uc.show_device_info("not-here")

            assert str(e.value) == "'not-here'"

        def test_success(self, device_uc: DeviceUsecases, device: Device):
            device.id = "id"
            device_uc.repo.store.devices[device.id] = device

            info = device_uc.show_device_info("id")

            assert info == "Device(id='id', hub=None)"

    class TestListDevices:
        def test_empty(self, device_uc: DeviceUsecases):
            assert device_uc.list_devices() == []

        def test_some(self, device_uc: DeviceUsecases):
            device_1 = Device(id="1")
            device_2 = Device(id="2")
            device_uc.repo.store.devices = {
                device_1.id: device_1,
                device_2.id: device_2,
            }

            devices = device_uc.list_devices()

            assert devices == [device_1, device_2]

    class TestUpdateDevice:
        def test_not_there(self, device_uc: DeviceUsecases):
            with pytest.raises(KeyError) as e:
                device_uc.update_device("not-here")

            assert str(e.value) == "'not-here'"

        def test_success(self, device_uc: DeviceUsecases):
            device = Lock(id="id", state=LockState.UNLOCKED)
            device_uc.repo.store.devices[device.id] = device
            expected = Lock(id="id", state=LockState.LOCKED)

            device = device_uc.update_device("id", state=LockState.LOCKED)

            assert device == expected
            assert device_uc.repo.store.devices == {expected.id: expected}
