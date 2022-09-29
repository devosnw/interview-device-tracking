from dataclasses import dataclass
from typing import Sequence

from idt.domains import Device, Dwelling, Hub, TypeDevice
from idt.repositories import DeviceRepository, DwellingRepository, HubRepository


@dataclass
class DeviceUsecases:
    repo: DeviceRepository

    def create_device(self, device_cls: type[TypeDevice], **kwargs) -> TypeDevice:
        pass

    def delete_device(self, id_: str):
        pass

    def show_device_info(self, id_: str) -> str:
        pass

    def list_devices(self) -> Sequence[TypeDevice]:
        pass

    def update_device(self, id_: str, **kwargs) -> str:
        pass


@dataclass
class HubUsecases:
    repo: HubRepository

    def list_hub_devices(self, id_: str) -> Sequence[TypeDevice]:
        pass

    def pair_device_to_hub(self, device: TypeDevice, hub: Hub):
        pass

    def unpair_device_from_hub(self, device: TypeDevice, hub: Hub):
        pass


@dataclass
class DwellingUsecases:
    repo: DwellingRepository

    def add_hub_to_dwelling(self, hub: Hub, dwelling: Dwelling):
        pass

    def list_dwelling_hubs(self, id_: str) -> Sequence(Hub):
        pass

    def occupy_dwelling(self, dwelling: Dwelling):
        pass

    def vacate_dwelling(self, dwelling: Dwelling):
        pass
