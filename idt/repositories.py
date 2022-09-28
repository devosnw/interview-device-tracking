from typing import Sequence, Type
import uuid

from idt.domains import Device, TypeDevices


_DEVICES: TypeDevices = {}


class DeviceRepository:
    def create(self, device: Type[Device]):
        if device.id is not None:
            raise ValueError(f"Device exists id={device.id}")

        device.id = uuid.uuid4()
        _DEVICES[device.id] = device
        return device

    def delete(self, id_: str):
        # TODO: if associated with hub, blow up
        del _DEVICES[id_]

    def get(self, id_: str) -> Device:
        return _DEVICES[id_]

    def list(self) -> Sequence[Device]:
        return [device for _, device in _DEVICES.items()]
