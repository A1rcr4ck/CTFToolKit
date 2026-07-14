from capstone import (
    Cs,
    CS_ARCH_X86,
    CS_MODE_32,
    CS_MODE_64,
)

from rev.reader import BinaryReader
from rev.models import Instruction


class Disassembler:

    def __init__(self, parser, resolver=None):

        self.parser = parser
        self.resolver = resolver
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

        # Required for future analysis
        self.cs.detail = True

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
                Instruction(
                    address=ins.address,
                    size=ins.size,
                    bytes=ins.bytes,
                    mnemonic=ins.mnemonic,
                    operands=self._format_operand(
                        ins.op_str
                    ),
                )
            )

            if len(instructions) >= count:
                break

        return instructions

    def section_legacy(
        self,
        name: str,
        count: int = 50,
    ):

        """
        Compatibility wrapper for older plugins/tests.
        Remove after migrating everything to Instruction.
        """

        return [
            (
                ins.address,
                ins.bytes.hex(" "),
                ins.mnemonic,
                ins.operands,
            )
            for ins in self.section(name, count)
        ]
    
    def _format_operand(self, operand: str):

        if self.resolver is None:
            return operand

        try:

            value = int(operand, 16)

        except ValueError:

            return operand

        symbol = self.resolver.resolve(value)

        if symbol:

            return symbol

        return operand