from rev.instructions import InstructionIndex


class InstructionDatabase:

    def __init__(self, parser):

        self.instructions = InstructionIndex(parser).all()

        self._address_map = {
            ins.address: ins
            for ins in self.instructions
        }

    def all(self):

        return self.instructions

    def by_address(self, address):

        return self._address_map.get(address)

    def mnemonic(self, mnemonic):

        return [
            ins
            for ins in self.instructions
            if ins.mnemonic == mnemonic
        ]