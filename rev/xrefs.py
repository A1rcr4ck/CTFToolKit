from rev.instructions import InstructionIndex


class XRefFinder:

    def __init__(self, parser):

        self.index = InstructionIndex(parser)

    def calls(self, target):

        refs = []

        for ins in self.index.all():

            if (
                ins.mnemonic == "call"
                and target.lower() in ins.operands.lower()
            ):

                refs.append(ins)

        return refs

    def jumps(self, target):

        refs = []

        for ins in self.index.all():

            if (
                ins.mnemonic.startswith("j")
                and target.lower() in ins.operands.lower()
            ):

                refs.append(ins)

        return refs