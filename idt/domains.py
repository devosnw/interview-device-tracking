from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Mapping, Optional, Sequence, Type

TypeDevices = Mapping[str, Type["Device"]]
TypeHubs = Sequence["Hub"]


@dataclass(kw_only=True)
class Device:
    id: Optional[str] = None
    hub: Optional["Hub"] = None


class SwitchState(Enum):
    OFF = auto()
    ON = auto()


@dataclass(kw_only=True)
class Switch(Device):
    state: SwitchState = SwitchState.OFF


@dataclass(kw_only=True)
class Dimmer(Device):
    brightness: int  # TODO: validate this within range with a setter


class LockState(Enum):
    UNLOCKED = auto()
    LOCKED = auto()


@dataclass(kw_only=True)
class Lock(Device):
    state: LockState = LockState.UNLOCKED
    code: Sequence[str] = field(default_factory=list)


@dataclass(kw_only=True)
class Thermostat(Device):
    target_temp_f: float  # TODO: validate this within range with a setter
    actual_temp_f: float  # TODO: validate this within range with a setter


@dataclass(kw_only=True)
class Hub:
    id: Optional[str] = None
    devices: TypeDevices = field(default_factory=list)
    dwelling: Optional["Dwelling"] = None

    def __post_init__(self):
        for device in self.devices:
            device.hub = self


@dataclass(kw_only=True)
class Dwelling:
    id: Optional[str] = None
    hubs: TypeHubs = field(default_factory=list)

    def __post_init__(self):
        for hub in self.hubs:
            hub.dwelling = self
