import sys
from TNF.src.tnf import TNF
from tools import read_benchmark_file



def execute():

    initial_formula, safety_formula, _ = read_benchmark_file(sys.argv[1])
    formula_str = " && ".join(initial_formula + safety_formula)
    TNF(formula_str, info=dict(), activated_apply_subsumptions=False, activated_print_info=False, activated_print_tnf=True, activate_verification=False)

execute()