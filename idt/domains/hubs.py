from dataclasses import dataclass, field
from typing import Sequence, Type


from idt.domains.devices import Device


@dataclass
class Hub:
    devices: Sequence[Type[Device]] = field(default_factory=list)
