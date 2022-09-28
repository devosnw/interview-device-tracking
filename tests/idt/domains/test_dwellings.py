from idt.domains.dwellings import Dwelling
from idt.domains.hubs import Hub


class TestDwelling:
    class TestInit:
        def test_defaults(self):
            dwelling = Dwelling()

            assert dwelling.hubs == []

        def test_fields(self):
            hubs = [Hub(), Hub()]

            dwelling = Dwelling(hubs=hubs)

            assert dwelling.hubs == hubs
