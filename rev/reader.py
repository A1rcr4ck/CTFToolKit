from rev.memory import MemoryRegion


class BinaryReader:

    def __init__(self, regions):

        self.regions = regions

    def region(self, name):

        for region in self.regions:

            if region.name == name:
                return region

        return None

    def read(self, address, size):

        for region in self.regions:

            start = region.virtual_address
            end = start + region.virtual_size

            if start <= address < end:

                offset = address - start

                return region.data[
                    offset:
                    offset + size
                ]

        return b""