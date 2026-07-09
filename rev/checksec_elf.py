from rev.elf import ELFParser


class ELFChecksec:

    def __init__(self, path):
        self.elf = ELFParser(path)

    def relro(self):

        has_gnu_relro = any(
            ph.type == "GNU_RELRO"
            for ph in self.elf.program_headers
        )

        bind_now = any(
            entry.tag == 24
            for entry in self.elf.dynamic
        )

        if has_gnu_relro and bind_now:
            return "Full"

        if has_gnu_relro:
            return "Partial"

        return "None"

    def nx(self):

        for ph in self.elf.program_headers:

            if ph.type == "GNU_STACK":

                return not (ph.flags & 0x1)

        return False

    def pie(self):

        return self.elf.header.type == "DYN"

    def canary(self):

        for symbol in self.elf.symbols:

            if symbol.name == "__stack_chk_fail":
                return True

        return False

    def rpath(self):

        for entry in self.elf.dynamic:

            if entry.tag == 15:
                return True

        return False

    def runpath(self):

        for entry in self.elf.dynamic:

            if entry.tag == 29:
                return True

        return False

    def result(self):

        return {
            "RELRO": self.relro(),
            "NX": self.nx(),
            "PIE": self.pie(),
            "Canary": self.canary(),
            "RPATH": self.rpath(),
            "RUNPATH": self.runpath(),
        }