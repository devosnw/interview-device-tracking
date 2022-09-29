from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Mapping, Optional, Sequence, TypeVar

TypeDevice = TypeVar("TypeDevice", bound="Device")


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
    devices: Mapping[str, TypeDevice] = field(default_factory=dict)
    dwelling: Optional["Dwelling"] = None

    def __post_init__(self):
        for device in self.devices.values():
            device.hub = self


@dataclass(kw_only=True)
class Dwelling:
    id: Optional[str] = None
    hubs: Mapping[str, Hub] = field(default_factory=dict)

    def __post_init__(self):
        for hub in self.hubs.values():
            hub.dwelling = self
