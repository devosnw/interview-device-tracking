from dataclasses import dataclass, field
from typing import Mapping, Sequence
import uuid

from idt.domains import Device, Dwelling, Hub, TypeDevice


@dataclass
class Store:
    devices: Mapping[str, Device] = field(default_factory=dict)
    dwellings: Mapping[str, Dwelling] = field(default_factory=dict)
    hubs: Mapping[str, Hub] = field(default_factory=dict)


@dataclass
class DeviceRepository:
    store: Store

    def create(self, device: TypeDevice) -> TypeDevice:
        if device.id is not None:
            raise ValueError(f"Device exists: id={device.id}")

        device.id = uuid.uuid4()
        self.save(device)
        return device

    def delete(self, device: TypeDevice):
        if device.hub is not None:
            raise ValueError(
                f"Device associated with a hub: id={device.id} hub_id={device.hub.id}"
            )
        del self.store.devices[device.id]

    def get(self, id_: str) -> TypeDevice:
        return self.store.devices[id_]

    def list(self) -> Sequence[TypeDevice]:
        return [device for _, device in self.store.devices.items()]

    def save(self, device: TypeDevice):
        self.store.devices[device.id] = device


@dataclass
class HubRepository:
    store: Store

    def get(self, id_: str) -> Hub:
        return self.store.hubs[id_]

    def save(self, hub: Hub):
        self.store.hubs[hub.id] = hub
        for _, device in hub.devices.items():
            self.store.devices[device.id] = device


@dataclass
class DwellingRepository:
    store: Store

    def get(self, id_: str) -> Dwelling:
        return self.store.dwellings[id_]

    def list(self) -> Sequence[Dwelling]:
        return [dwelling for _, dwelling in self.store.dwellings.items()]

    def save(self, dwelling: Dwelling):
        self.store.dwellings[dwelling.id] = dwelling
        for _, hub in dwelling.hubs.items():
            self.store.hubs[hub.id] = hub
            for _, device in hub.devices.items():
                self.store.devices[device.id] = device
