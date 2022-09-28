from typing import Sequence
import uuid

from idt.domains import Device, TypeDevice, TypeDevices


_DEVICES: TypeDevices = {}


class DeviceRepository:
    def create(self, device: TypeDevice):
        if device.id is not None:
            raise ValueError(f"Device exists id={device.id}")

        device.id = uuid.uuid4()
        _DEVICES[device.id] = device
        return device

    def delete(self, device: TypeDevice):
        if device.hub is not None:
            raise ValueError(
                f"Device associated with a hub id={device.id} hub_id={device.hub.id}"
            )
        del _DEVICES[device.id]

    def get(self, id_: str) -> Device:
        return _DEVICES[id_]

    def list(self) -> Sequence[Device]:
        return [device for _, device in _DEVICES.items()]
