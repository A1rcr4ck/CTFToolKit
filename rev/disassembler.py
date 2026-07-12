from capstone import (
    Cs,
    CS_ARCH_X86,
    CS_MODE_32,
    CS_MODE_64,
)

from rev.reader import BinaryReader


class Disassembler:

    def __init__(self, parser):

        self.parser = parser
        self.reader = BinaryReader(parser.memory)

        machine = parser.header.machine

        if machine in ("AMD x86-64", "x86-64"):
            self.cs = Cs(
                CS_ARCH_X86,
                CS_MODE_64,
            )

        elif machine in ("Intel 80386", "x86"):
            self.cs = Cs(
                CS_ARCH_X86,
                CS_MODE_32,
            )

        else:
            raise NotImplementedError(machine)

    def section(
        self,
        name: str,
        count: int = 50,
    ):

        region = self.reader.region(name)

        if region is None:
            raise ValueError(name)

        instructions = []

        for ins in self.cs.disasm(
            region.data,
            region.virtual_address,
        ):

            instructions.append(
                (
                    ins.address,
                    ins.bytes.hex(" "),
                    ins.mnemonic,
                    ins.op_str,
                )
            )

            if len(instructions) >= count:
                break

        return instructions