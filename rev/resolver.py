class SymbolResolver:

    def __init__(self, parser):

        self.parser = parser

        self._symbols = {}

        self._build()

    def _build(self):

        #
        # ELF Symbols
        #

        if hasattr(self.parser, "symbols"):

            for symbol in self.parser.symbols:

                if symbol.value:

                    self._symbols[symbol.value] = symbol.name

        #
        # PE Exports
        #

        if hasattr(self.parser, "exports"):

            for export in self.parser.exports:

                self._symbols[export.address] = export.name

    def resolve(self, address):

        return self._symbols.get(address)

    @property
    def symbols(self):

        return self._symbols