from .info import register_info
from .hashes import register_hashes
from .entropy import register_entropy
from .strings import register_strings
from .checksec import register_checksec
from .sections import register_sections
from .imports import register_imports
from .exports import register_exports
from .resources import register_resources
from .symbols import register_symbols
from .dynamic import register_dynamic
from .relocations import register_relocations
from .program_headers import register_program_headers
from .elf_header import register_elf_header
from .pe_header import register_pe_header
from .disassemble import register_disassemble
from .hexdump import register_hexdump

def register(subparsers):
    reverse = subparsers.add_parser(
        "reverse",
        help="Reverse engineering utilities"
    )

    reverse_sub = reverse.add_subparsers(
        dest="command",
        required=True
    )
   
    register_info(reverse_sub)
    register_hashes(reverse_sub)
    register_entropy(reverse_sub)
    register_strings(reverse_sub)
    register_checksec(reverse_sub)
    register_sections(reverse_sub)
    register_imports(reverse_sub)
    register_exports(reverse_sub)
    register_resources(reverse_sub)
    register_symbols(reverse_sub)
    register_dynamic(reverse_sub)
    register_relocations(reverse_sub)
    register_program_headers(reverse_sub)
    register_elf_header(reverse_sub)
    register_pe_header(reverse_sub)
    register_disassemble(reverse_sub)
    register_hexdump(reverse_sub)
