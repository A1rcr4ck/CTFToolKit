from rev.disassembler import Disassembler


class InstructionSearcher:

    def __init__(self, parser):

        self.disassembler = Disassembler(parser)

    def mnemonic(self, section=".text", mnemonic=""):

        results = []

        for ins in self.disassembler.section(section):

            if ins.mnemonic.lower() == mnemonic.lower():

                results.append(ins)

        return results

    def operand(self, section=".text", text=""):

        results = []

        for ins in self.disassembler.section(section):

            if text.lower() in ins.operands.lower():

                results.append(ins)

        return results