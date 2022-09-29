import pytest
from pytest_mock import MockerFixture

from idt.domains import Device, Dwelling, Hub, Lock, LockState
from idt.repositories import DeviceRepository, DwellingRepository, HubRepository, Store


@pytest.fixture
def device_repo(store) -> DeviceRepository:
    return DeviceRepository(store)


@pytest.fixture
def device() -> Device:
    return Device()


@pytest.fixture
def dwelling_repo(store) -> DwellingRepository:
    return DwellingRepository(store)


@pytest.fixture
def dwelling() -> Dwelling:
    return Dwelling()


@pytest.fixture
def hub_repo(store) -> HubRepository:
    return HubRepository(store)


@pytest.fixture
def hub() -> Hub:
    return Hub()


@pytest.fixture
def store() -> Store:
    return Store()


class TestDeviceRepository:
    def test_init(self):
        assert DeviceRepository(Store()) is not None

    class TestCreate:
        def test_existing(self, device_repo: DeviceRepository, device: Device):
            device.id = "exists"

            with pytest.raises(ValueError) as e:
                device_repo.create(device)

            assert str(e.value) == "Device exists: id=exists"

        def test_success(
            self,
            mocker: MockerFixture,
            device_repo: DeviceRepository,
            device: Device,
        ):
            mocker.patch("idt.repositories.uuid.uuid4", return_value="a-uuid")

            device = device_repo.create(device)

            assert device.id == "a-uuid"
            assert device_repo.store.devices == {"a-uuid": device}

    class TestDelete:
        def test_associated(self, device_repo: DeviceRepository, device: Device):
            device.id = "id"
            device.hub = Hub(id="hub_id")

            with pytest.raises(ValueError) as e:
                device_repo.delete(device)

            assert str(e.value) == "Device associated with a hub: id=id hub_id=hub_id"

        def test_not_found(self, device_repo: DeviceRepository, device: Device):
            device.id = "not-here"

            with pytest.raises(KeyError) as e:
                device_repo.delete(device)

            assert str(e.value) == "'not-here'"

        def test_found(
            self,
            device_repo: DeviceRepository,
            device: Device,
        ):
            device.id = "id"
            device_repo.store.devices["id"] = device

            device_repo.delete(device)

            assert device_repo.store.devices == {}

    class TestGet:
        def test_not_found(self, device_repo: DeviceRepository):
            with pytest.raises(KeyError) as e:
                device_repo.get("not-here")

            assert str(e.value) == "'not-here'"

        def test_found(self, device_repo: DeviceRepository, device: Device):
            device.id = "id"
            device_repo.store.devices[device.id] = device

            assert device_repo.get("id") == device

    class TestList:
        def test_empty(self, device_repo: DeviceRepository):
            assert device_repo.list() == []

        def test_some(self, device_repo: DeviceRepository):
            device_1 = Device(id="1")
            device_2 = Device(id="2")
            device_repo.store.devices = {
                device_1.id: device_1,
                device_2.id: device_2,
            }

            devices = device_repo.list()

            assert devices == [device_1, device_2]

    class TestSave:
        def test_success(self, device_repo: DeviceRepository):
            device = Lock(id="id", state=LockState.UNLOCKED)
            device_repo.store.devices[device.id] = device
            device.state = LockState.LOCKED

            device_repo.save(device)

            assert device_repo.store.devices[device.id].state == LockState.LOCKED


class TestHubRepository:
    def test_init(self):
        assert HubRepository(Store()) is not None

    class TestGet:
        def test_not_found(self, hub_repo: HubRepository):
            with pytest.raises(KeyError) as e:
                hub_repo.get("not-here")

            assert str(e.value) == "'not-here'"

        def test_found(self, hub_repo: HubRepository, hub: Hub):
            hub.id = "id"
            hub_repo.store.hubs[hub.id] = hub

            assert hub_repo.get("id") == hub

    class TestSave:
        def test_success(self, hub_repo: HubRepository, hub: Hub):
            hub_repo.store.hubs[hub.id] = hub
            expected = {"id": Device()}
            hub.devices = expected

            hub_repo.save(hub)

            assert hub_repo.store.hubs[hub.id].devices == expected


class TestDwellingRepository:
    def test_init(self):
        assert DwellingRepository(Store()) is not None

    class TestGet:
        def test_not_found(self, dwelling_repo: DwellingRepository):
            with pytest.raises(KeyError) as e:
                dwelling_repo.get("not-here")

            assert str(e.value) == "'not-here'"

        def test_found(self, dwelling_repo: DwellingRepository, dwelling: Dwelling):
            dwelling.id = "id"
            dwelling_repo.store.dwellings[dwelling.id] = dwelling

            assert dwelling_repo.get("id") == dwelling

    class TestList:
        def test_empty(self, dwelling_repo: DwellingRepository):
            assert dwelling_repo.list() == []

        def test_some(self, dwelling_repo: DwellingRepository):
            dwelling_1 = Dwelling(id="1")
            dwelling_2 = Dwelling(id="2")
            dwelling_repo.store.dwellings = {
                dwelling_1.id: dwelling_1,
                dwelling_2.id: dwelling_2,
            }

            dwellings = dwelling_repo.list()

            assert dwellings == [dwelling_1, dwelling_2]

    class TestSave:
        def test_success(self, dwelling_repo: DwellingRepository, dwelling: Dwelling):
            dwelling_repo.store.dwellings[dwelling.id] = dwelling
            expected = {"id": Hub()}
            dwelling.hubs = expected

            dwelling_repo.save(dwelling)

            assert dwelling_repo.store.dwellings[dwelling.id].hubs == expected
