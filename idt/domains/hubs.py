from dataclasses import dataclass
from typing import List, Type


from idt.domains.devices import Device


@dataclass
class Hub:
    devices: List[Type[Device]]
