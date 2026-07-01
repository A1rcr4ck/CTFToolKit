from crypto.solver import CryptoSolver
from core.input import read_input

def run_solver(args):

    history = CryptoSolver().solve(read_input(args.text))

    if not history:
        print("Nothing decoded.")
        return

    print(f"{'Step':<5}{'Encoding':<12}Output")
    print("-" * 70)

    for i, (encoding, decoded) in enumerate(history, 1):
        print(f"{i:<5}{encoding:<12}{decoded}")