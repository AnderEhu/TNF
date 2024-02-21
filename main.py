import sys
from TNF.src.tnf import TNF
from tools import read_benchmark_file


def execute():

    initial_formula, safety_formula, _ = read_benchmark_file(sys.argv[1])

    initial_formula_str = f'{" && ".join(initial_formula)}'
    safety_formula_str = f'{" && ".join(safety_formula)}'

    formula_str = f"({initial_formula_str}) && ({safety_formula_str})"
    TNF(formula_str, info=dict(), activated_apply_subsumptions=False,
        activated_print_info=False, activated_print_tnf=True, activate_verification=False)


execute()
