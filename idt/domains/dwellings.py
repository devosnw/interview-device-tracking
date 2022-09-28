from dataclasses import dataclass, field
from typing import Sequence

from idt.domains.hubs import Hub


@dataclass
class Dwelling:
    hubs: Sequence[Hub] = field(default_factory=list)
