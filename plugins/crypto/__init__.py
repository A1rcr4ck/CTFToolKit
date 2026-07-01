from .base import register_base
from .classical import register_classical
from .xor import register_xor
from .detect import register_detect
from .hash import register_hash
from .analyzer import register_analyzer
from .identify import register_identify
from .solve import register_solver

def register(subparsers):
    crypto = subparsers.add_parser(
        "crypto",
        help="Crypto Toolkit"
    )

    crypto_sub = crypto.add_subparsers(
        dest="algorithm",
        required=True
    )

    register_base(crypto_sub)
    register_classical(crypto_sub)
    register_xor(crypto_sub)
    register_detect(crypto_sub)
    register_hash(crypto_sub)
    register_analyzer(crypto_sub)
    register_identify(crypto_sub)
    register_solver(crypto_sub)