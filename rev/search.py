from rev.disassembler import Disassembler


class InstructionSearcher:

    def __init__(self, parser):

        self.disassembler = Disassembler(parser)

    def mnemonic(self, section=".text", mnemonic=""):

        results = []

        for addr, bytes_, ins, operands in self.disassembler.section(section):

            if ins.lower() == mnemonic.lower():

                results.append(
                    (
                        addr,
                        bytes_,
                        ins,
                        operands,
                    )
                )

        return results

    def operand(self, section=".text", text=""):

        results = []

        for addr, bytes_, ins, operands in self.disassembler.section(section):

            if text.lower() in operands.lower():

                results.append(
                    (
                        addr,
                        bytes_,
                        ins,
                        operands,
                    )
                )

        return results