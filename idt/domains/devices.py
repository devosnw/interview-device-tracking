from dataclasses import dataclass
from typing import Optional


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
