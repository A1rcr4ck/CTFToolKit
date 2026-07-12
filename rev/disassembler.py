from capstone import (
    Cs,
    CS_ARCH_X86,
    CS_MODE_32,
    CS_MODE_64,
)


class Disassembler:

    def __init__(self, parser):

        self.parser = parser

        if parser.header.machine in (
            "AMD x86-64",
            "x86-64",
        ):
            self.cs = Cs(
                CS_ARCH_X86,
                CS_MODE_64,
            )

        elif parser.header.machine in (
            "Intel 80386",
            "x86",
        ):
            self.cs = Cs(
                CS_ARCH_X86,
                CS_MODE_32,
            )

        else:
            raise NotImplementedError(
                parser.header.machine
            )

    def disassemble(
        self,
        region,
        count=20,
    ):

        instructions = []

        for ins in self.cs.disasm(
            region.data,
            region.virtual_address,
        ):

            instructions.append(
                (
                    ins.address,
                    ins.mnemonic,
                    ins.op_str,
                )
            )

            if len(instructions) >= count:
                break

        return instructions