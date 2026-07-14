from rev.parser import BinaryParser
from rev.reader import BinaryReader
from rev.disassembler import Disassembler
from rev.instructions import InstructionIndex
from rev.functions import FunctionFinder


class ReverseEngine:

    def __init__(self, path):

        self.parser = BinaryParser.open(path)

        self.reader = BinaryReader(
            self.parser.memory
        )

        self.disassembler = Disassembler(
            self.parser
        )

        self.instructions = InstructionIndex(
            self.parser
        )

        self.functions = FunctionFinder(
            self.parser
        )