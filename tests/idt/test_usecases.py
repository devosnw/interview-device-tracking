from typing import Mapping
import pytest
from pytest_mock import MockerFixture

from idt.domains import (
    Device,
    Dimmer,
    Dwelling,
    DwellingState,
    Hub,
    Lock,
    LockState,
    Switch,
    SwitchState,
    Thermostat,
    TypeDevice,
)
from idt.repositories import DeviceRepository, DwellingRepository, HubRepository, Store
from idt.usecases import DeviceUsecases, DwellingUsecases, HubUsecases


@pytest.fixture
def device_repo(store) -> DeviceRepository:
    return DeviceRepository(store)


@pytest.fixture
def device_uc(device_repo: DeviceRepository) -> DeviceUsecases:
    return DeviceUsecases(device_repo)


@pytest.fixture
def device() -> Device:
    return Device()


@pytest.fixture
def dwelling_repo(store) -> DwellingRepository:
    return DwellingRepository(store)


@pytest.fixture
def dwelling_uc(dwelling_repo, hub_repo) -> DwellingUsecases:
    return DwellingUsecases(dwelling_repo, hub_repo)


@pytest.fixture
def dwelling() -> Dwelling:
    return Dwelling()


@pytest.fixture
def hub_repo(store) -> HubRepository:
    return HubRepository(store)


@pytest.fixture
def hub_uc(hub_repo, device_repo) -> HubUsecases:
    return HubUsecases(hub_repo, device_repo)


@pytest.fixture
def hub() -> Hub:
    return Hub()


@pytest.fixture
def mock_uuid(mocker: MockerFixture):
    return mocker.patch("idt.repositories.uuid.uuid4", return_value="a-uuid")


@pytest.fixture
def store() -> Store:
    return Store()


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

            device_uc.update_device("id", state=LockState.LOCKED)

            assert device_uc.repo.store.devices == {expected.id: expected}


class TestHubUsecases:
    def test_init(self, hub_repo, device_repo):
        assert HubUsecases(hub_repo, device_repo) is not None

    class TestListHubDevices:
        def test_not_there(self, hub_uc: HubUsecases):
            with pytest.raises(KeyError) as e:
                hub_uc.list_hub_devices("not-here")

            assert str(e.value) == "'not-here'"

        def test_empty(self, hub_uc: HubUsecases, hub: Hub):
            hub.id = "id"
            hub_uc.repo.store.hubs[hub.id] = hub

            assert hub_uc.list_hub_devices("id") == []

        def test_some(self, hub_uc: HubUsecases):
            device_1 = Device(id="1")
            device_2 = Device(id="2")
            hub = Hub(
                id="id",
                devices={
                    device_1.id: device_1,
                    device_2.id: device_2,
                },
            )
            hub_uc.repo.store.hubs[hub.id] = hub

            assert hub_uc.list_hub_devices("id") == [device_1, device_2]

    class TestPairDevice:
        def test_not_there(self, hub_uc: HubUsecases):
            with pytest.raises(KeyError) as e:
                hub_uc.pair_device("not-here", "")

            assert str(e.value) == "'not-here'"

        def test_device_not_there(self, hub_uc: HubUsecases, hub: Hub):
            hub.id = "id"
            hub_uc.repo.store.hubs[hub.id] = hub

            with pytest.raises(KeyError) as e:
                hub_uc.pair_device("id", "not-here")

            assert str(e.value) == "'not-here'"

        def test_success(self, hub_uc: HubUsecases, hub: Hub, device: Device):
            hub.id = "id"
            hub_uc.repo.store.hubs[hub.id] = hub
            device.id = "device-id"
            hub_uc.device_repo.store.devices[device.id] = device

            hub_uc.pair_device("id", "device-id")

            assert hub_uc.repo.store.hubs["id"].devices == {device.id: device}
            assert hub_uc.device_repo.store.devices["device-id"].hub == hub

    class TestUnpairDevice:
        def test_not_there(self, hub_uc: HubUsecases):
            with pytest.raises(KeyError) as e:
                hub_uc.unpair_device("not-here", "")

            assert str(e.value) == "'not-here'"

        def test_device_not_there(self, hub_uc: HubUsecases, hub: Hub):
            hub.id = "id"
            hub_uc.repo.store.hubs[hub.id] = hub

            with pytest.raises(KeyError) as e:
                hub_uc.unpair_device("id", "not-here")

            assert str(e.value) == "'not-here'"

        def test_success(self, hub_uc: HubUsecases, hub: Hub, device: Device):
            device.id = "device-id"
            hub.id = "id"
            hub.pair_device(device)
            hub_uc.device_repo.store.devices[device.id] = device
            hub_uc.repo.store.hubs[hub.id] = hub

            hub_uc.unpair_device("id", "device-id")

            assert hub_uc.repo.store.hubs["id"].devices == {}
            assert hub_uc.device_repo.store.devices["device-id"].hub is None


class TestDwellingUsecases:
    def test_init(self, dwelling_repo, hub_repo):
        dwelling_uc = DwellingUsecases(dwelling_repo, hub_repo)

        assert dwelling_uc.repo == dwelling_repo
        assert dwelling_uc.hub_repo == hub_repo

    class TestInstallHub:
        def test_not_there(self, dwelling_uc: DwellingUsecases):
            with pytest.raises(KeyError) as e:
                dwelling_uc.install_hub("not-here", "")

            assert str(e.value) == "'not-here'"

        def test_hub_not_there(self, dwelling_uc: DwellingUsecases, dwelling: Dwelling):
            dwelling.id = "id"
            dwelling_uc.repo.store.dwellings[dwelling.id] = dwelling

            with pytest.raises(KeyError) as e:
                dwelling_uc.install_hub("id", "not-here")

            assert str(e.value) == "'not-here'"

        def test_success(
            self, dwelling_uc: DwellingUsecases, dwelling: Dwelling, hub: Hub
        ):
            dwelling.id = "id"
            dwelling_uc.repo.store.dwellings[dwelling.id] = dwelling
            hub.id = "hub-id"
            dwelling_uc.repo.store.hubs[hub.id] = hub

            dwelling_uc.install_hub("id", "hub-id")

            assert dwelling_uc.repo.store.dwellings["id"].hubs == {hub.id: hub}
            assert dwelling_uc.repo.store.hubs[hub.id].dwelling == dwelling

    class TestListDwellings:
        def test_empty(self, dwelling_uc: DwellingUsecases):
            assert dwelling_uc.list_dwellings() == []

        def test_some(self, dwelling_uc: DwellingUsecases):
            dwelling_1 = Dwelling(id="1")
            dwelling_2 = Dwelling(id="2")
            dwelling_uc.repo.store.dwellings = {
                dwelling_1.id: dwelling_1,
                dwelling_2.id: dwelling_2,
            }

            assert dwelling_uc.list_dwellings() == [dwelling_1, dwelling_2]

    class TestOccupy:
        def test_not_there(self, dwelling_uc: DwellingUsecases):
            with pytest.raises(KeyError) as e:
                dwelling_uc.occupy("not-here")

            assert str(e.value) == "'not-here'"

        def test_success(self, dwelling_uc: DwellingUsecases, dwelling: Dwelling):
            dwelling.id = "id"
            dwelling.state = DwellingState.VACANT
            dwelling_uc.repo.store.dwellings[dwelling.id] = dwelling

            dwelling_uc.occupy("id")

            assert (
                dwelling_uc.repo.store.dwellings["id"].state == DwellingState.OCCUPIED
            )

    class TestVacate:
        def test_not_there(self, dwelling_uc: DwellingUsecases):
            with pytest.raises(KeyError) as e:
                dwelling_uc.vacate("not-here")

            assert str(e.value) == "'not-here'"

        def test_success(self, dwelling_uc: DwellingUsecases, dwelling: Dwelling):
            dwelling.id = "id"
            dwelling.state = DwellingState.OCCUPIED
            dwelling_uc.repo.store.dwellings[dwelling.id] = dwelling

            dwelling_uc.vacate("id")

            assert dwelling_uc.repo.store.dwellings["id"].state == DwellingState.VACANT
