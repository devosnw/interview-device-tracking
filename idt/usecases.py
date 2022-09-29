from dataclasses import dataclass
from typing import Sequence

from idt.domains import Device, Dwelling, Hub, TypeDevice
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

    def install_hub(self, id_: str, hub_id: str):
        pass

    def list_dwellings(self) -> Sequence[Dwelling]:
        pass

    def occupy(self, id_: str):
        pass

    def vacate(self, id_: str):
        pass
