from rev.disassembler import Disassembler


class FunctionFinder:

    def __init__(self, parser):

        self.parser = parser
        self.disassembler = Disassembler(parser)

    def from_symbols(self):

        functions = []

        if not hasattr(self.parser, "symbols"):
            return functions

        for symbol in self.parser.symbols:

            if (
                symbol.type == "FUNC"
                and symbol.value != 0
            ):

                functions.append(
                    {
                        "name": symbol.name,
                        "address": symbol.value,
                        "size": symbol.size,
                        "source": "symbol",
                    }
                )

        return functions

    def from_exports(self):

        functions = []

        if not hasattr(self.parser, "exports"):
            return functions

        for export in self.parser.exports:

            functions.append(
                {
                    "name": export.name,
                    "address": export.address,
                    "size": 0,
                    "source": "export",
                }
            )

        return functions

    def find(self):

        functions = []

        functions.extend(
            self.from_symbols()
        )

        functions.extend(
            self.from_exports()
        )

        functions.sort(
            key=lambda x: x["address"]
        )

        return functions