import pytest
from pytest_mock import MockerFixture

from idt.domains import (
    Dimmer,
    Dwelling,
    DwellingState,
    Hub,
    Lock,
    LockState,
    Switch,
    SwitchState,
    Thermostat,
)
from idt.repositories import DeviceRepository, DwellingRepository, HubRepository, Store
from idt.usecases import DeviceUsecases, DwellingUsecases, HubUsecases


class UUID:
    count: int = 0

    def uuid(self) -> str:
        self.count += 1
        return f"uuid-{self.count}"


@pytest.fixture
def mock_uuid(mocker: MockerFixture, uuid: UUID):
    return mocker.patch("idt.repositories.uuid.uuid4", side_effect=uuid.uuid)


@pytest.fixture
def uuid() -> UUID:
    return UUID()


@pytest.mark.usefixtures("mock_uuid")
def test_solution(uuid: UUID):
    # base data
    hub = Hub(id=uuid.uuid())
    dwelling = Dwelling(id=uuid.uuid())
    store = Store(
        hubs={hub.id: hub},
        dwellings={dwelling.id: dwelling},
    )

    device_repo = DeviceRepository(store)
    hub_repo = HubRepository(store)
    dwelling_repo = DwellingRepository(store)

    device_uc = DeviceUsecases(device_repo)
    hub_uc = HubUsecases(hub_repo, device_repo)
    dwelling_uc = DwellingUsecases(dwelling_repo, hub_repo)

    # create some devices
    dimmer = device_uc.create_device(Dimmer, brightness=40)
    lock = device_uc.create_device(Lock, state=LockState.LOCKED, code=["1", "2", "3"])
    switch_ = device_uc.create_device(Switch, state=SwitchState.ON)
    thermo = device_uc.create_device(Thermostat, target_temp_f=68.0, actual_temp_f=75.0)

    # see how they're doing
    assert (
        device_uc.show_device_info(dimmer.id)
        == "Dimmer(id='uuid-3', hub=None, brightness=40)"
    )
    assert (
        device_uc.show_device_info(lock.id)
        == "Lock(id='uuid-4', hub=None, state=<LockState.LOCKED: 2>, code=['1', '2', '3'])"
    )

    # update it
    device_uc.update_device(dimmer.id, brightness=80)

    # see how they're doing
    assert (
        device_uc.show_device_info(dimmer.id)
        == "Dimmer(id='uuid-3', hub=None, brightness=80)"
    )

    # get them all
    assert device_uc.list_devices() == [dimmer, lock, switch_, thermo]

    # get rid of one
    device_uc.delete_device(dimmer.id)
    assert device_uc.list_devices() == [lock, switch_, thermo]

    # pair them
    hub_uc.pair_device(hub.id, lock.id)
    hub_uc.pair_device(hub.id, switch_.id)
    hub_uc.pair_device(hub.id, thermo.id)

    # can't delete it!
    with pytest.raises(ValueError):
        device_uc.delete_device(lock.id)

    # see how their doing
    assert hub_uc.list_hub_devices(hub.id) == [lock, switch_, thermo]

    # remove one
    hub_uc.unpair_device(hub.id, lock.id)
    assert hub_uc.list_hub_devices(hub.id) == [switch_, thermo]

    # show our dwellings
    assert dwelling_uc.list_dwellings() == [dwelling]

    # the dwelling is available
    dwelling_uc.vacate(dwelling.id)
    assert dwelling.state == DwellingState.VACANT

    # add our hub
    dwelling_uc.install_hub(dwelling.id, hub.id)
    assert len(dwelling.hubs) == 1

    # the tenant left
    dwelling_uc.vacate(dwelling.id)
    assert dwelling.state == DwellingState.VACANT
