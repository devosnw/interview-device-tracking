from dataclasses import dataclass
from typing import Sequence

from idt.domains import Dwelling, DwellingState, TypeDevice
from idt.repositories import DeviceRepository, DwellingRepository, HubRepository


@dataclass
class DeviceUsecases:
    repo: DeviceRepository

    def create_device(self, device_cls: type[TypeDevice], **attrs) -> TypeDevice:
        return self.repo.create(device_cls(**attrs))

    def delete_device(self, id_: str):
        self.repo.delete(self.repo.get(id_))

    def show_device_info(self, id_: str) -> str:
        return str(self.repo.get(id_))

    def list_devices(self) -> Sequence[TypeDevice]:
        return self.repo.list()

    def update_device(self, id_: str, **attrs):
        device = self.repo.get(id_)
        for attr, value in attrs.items():
            setattr(device, attr, value)
        self.repo.save(device)


@dataclass
class HubUsecases:
    repo: HubRepository
    device_repo: DeviceRepository

    def list_hub_devices(self, id_: str) -> Sequence[TypeDevice]:
        hub = self.repo.get(id_)
        return [hub for _, hub in hub.devices.items()]

    def pair_device(self, id_: str, device_id: str):
        hub = self.repo.get(id_)
        device = self.device_repo.get(device_id)

        hub.pair_device(device)
        self.repo.save(hub)

    def unpair_device(self, id_: str, device_id: str):
        hub = self.repo.get(id_)
        device = self.device_repo.get(device_id)

        hub.unpair_device(device)
        self.repo.save(hub)


@dataclass
class DwellingUsecases:
    repo: DwellingRepository
    hub_repo: HubRepository

    def install_hub(self, id_: str, hub_id: str):
        dwelling = self.repo.get(id_)
        hub = self.hub_repo.get(hub_id)

        dwelling.install_hub(hub)
        self.repo.save(dwelling)

    def list_dwellings(self) -> Sequence[Dwelling]:
        return self.repo.list()

    def occupy(self, id_: str):
        dwelling = self.repo.get(id_)
        dwelling.state = DwellingState.OCCUPIED
        self.repo.save(dwelling)

    def vacate(self, id_: str):
        dwelling = self.repo.get(id_)
        dwelling.state = DwellingState.VACANT
        self.repo.save(dwelling)
