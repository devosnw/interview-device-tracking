from typing import Mapping, Type
import uuid

from idt.domains.devices import Device


_DEVICES: Mapping[str, Type[Device]] = {}


class DeviceRepository:
    def create(self, device: Type[Device]):
        if device.id is not None:
            raise ValueError(f"Device exists id={device.id}")

        device.id = uuid.uuid4()
        _DEVICES[device.id] = device
        return device

    def delete(self):
        raise NotImplementedError()

    def get(self, id_: str) -> Device:
        return _DEVICES[id_]

    def list(self):
        raise NotImplementedError()
