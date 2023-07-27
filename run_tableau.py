import sys
from tools import read_benchmark_file



def execute():

    initial_formula, safety_formula, env_constraints = read_benchmark_file(sys.argv[1])

execute()