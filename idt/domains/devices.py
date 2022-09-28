from dataclasses import dataclass


@dataclass
class Device:
    pass


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
