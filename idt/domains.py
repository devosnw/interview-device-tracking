from dataclasses import dataclass
from enum import Enum, auto
from typing import Mapping, Optional, Sequence, Type

TypeDevices = Mapping[str, Type["Device"]]
TypeHubs = Sequence["Hub"]


@dataclass(kw_only=True)
class Device:
    id: str
    hub: Optional["Hub"]


class SwitchState(Enum):
    OFF = auto()
    ON = auto()


@dataclass(kw_only=True)
class Switch(Device):
    state: SwitchState


@dataclass(kw_only=True)
class Dimmer(Device):
    brightness: int  # TODO: validate this within range with a setter


class LockState(Enum):
    UNLOCKED = auto()
    LOCKED = auto()


@dataclass(kw_only=True)
class Lock(Device):
    state: LockState
    code: Sequence[str]


@dataclass(kw_only=True)
class Thermostat(Device):
    target_temp_f: float  # TODO: validate this within range with a setter
    actual_temp_f: float  # TODO: validate this within range with a setter


@dataclass(kw_only=True)
class Hub:
    id: str
    devices: TypeDevices
    dwelling: Optional["Dwelling"]

    def __post_init__(self):
        for device in self.devices:
            device.hub = self


@dataclass(kw_only=True)
class Dwelling:
    id: str
    hubs: TypeHubs

    def __post_init__(self):
        for hub in self.hubs:
            hub.dwelling = self
