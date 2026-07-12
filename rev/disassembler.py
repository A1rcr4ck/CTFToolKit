from capstone import *


class Disassembler:

    def __init__(self, arch, mode):

        self.cs = Cs(arch, mode)

    def disassemble(self, code, address):

        return list(
            self.cs.disasm(code, address)
        )