from rev.instructions import InstructionIndex


class ROPFinder:

    def __init__(self, parser):

        self.index = InstructionIndex(parser)

    def gadgets(self):

        instructions = self.index.all()

        gadgets = []

        for i, ins in enumerate(instructions):

            if ins.mnemonic != "ret":
                continue

            gadget = instructions[max(0, i - 3): i + 1]

            gadgets.append(gadget)

        return gadgets