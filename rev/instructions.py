from rev.disassembler import Disassembler


class InstructionIndex:

    def __init__(self, parser):

        self.parser = parser
        self.disassembler = Disassembler(parser)

    def all(self):

        instructions = []

        for section in self.parser.executable_sections:

            try:

                for ins in self.disassembler.section(
                    section.name
                ):

                    instructions.append(ins)

            except Exception:
                continue

        return instructions