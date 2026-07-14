from rev.disassembler import Disassembler


class InstructionIndex:

    def __init__(self, parser):

        self.parser = parser
        self.disassembler = Disassembler(parser)

        self._cache = None

    def all(self):

        if self._cache is not None:
            return self._cache

        instructions = []

        for section in self.parser.executable_sections:

            try:

                for ins in self.disassembler.section(
                    section.name
                ):

                    instructions.append(ins)

            except Exception:
                continue

        self._cache = instructions

        return self._cache