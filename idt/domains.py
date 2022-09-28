from dataclasses import dataclass, field
from typing import Optional, Sequence, Type


@dataclass
class Device:
    id: Optional[str] = None


@dataclass
class Switch(Device):
    pass


@dataclass
class Dimmer(Device):
    pass


@dataclass
class Lock(Device):
    pass


@dataclass
class Thermostat(Device):
    pass


@dataclass
class Hub:
    devices: Sequence[Type[Device]] = field(default_factory=list)


@dataclass
class Dwelling:
    hubs: Sequence[Hub] = field(default_factory=list)
