from rev.disassembler import Disassembler


class FunctionFinder:

    def __init__(self, parser):

        self.parser = parser
        self.dis = Disassembler(parser)

    def find(self):

        functions = []

        # ELF symbols
        if hasattr(self.parser, "symbols"):

            for sym in self.parser.symbols:

                if (
                    getattr(sym, "type", "") == "FUNC"
                    and sym.value != 0
                ):

                    functions.append(
                        (
                            sym.name,
                            sym.value,
                            sym.size,
                        )
                    )

        # PE exports
        if hasattr(self.parser, "exports"):

            for exp in self.parser.exports:

                functions.append(
                    (
                        exp.name,
                        exp.address,
                        0,
                    )
                )

        return sorted(
            functions,
            key=lambda x: x[1],
        )