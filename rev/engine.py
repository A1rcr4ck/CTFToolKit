from rev.parser import BinaryParser
from rev.reader import BinaryReader
from rev.disassembler import Disassembler
from rev.instructions import InstructionIndex
from rev.functions import FunctionFinder
from rev.resolver import SymbolResolver
from rev.instruction_db import InstructionDatabase


class ReverseEngine:

    def __init__(self, path):

        self.parser = BinaryParser.open(path)

        self.reader = BinaryReader(
            self.parser.memory
        )

        # Create the resolver first
        self.resolver = SymbolResolver(
            self.parser
        )

        # Then pass it to the disassembler
        self.disassembler = Disassembler(
            self.parser,
            self.resolver,
        )

        self.instructions = InstructionIndex(
            self.parser
        )

        self.functions = FunctionFinder(
            self.parser
        )

        self.database = InstructionDatabase(
            self.parser
        )

    @property
    def memory(self):
        return self.parser.memory

    @property
    def sections(self):
        return self.parser.sections

    @property
    def executable_sections(self):
        return self.parser.executable_sections

    @property
    def decoded_instructions(self):
        return self.instructions.all()