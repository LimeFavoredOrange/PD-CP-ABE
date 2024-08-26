import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', ".."))
if project_root not in sys.path: sys.path.append(project_root)

from PD_CP_ABE import PD_CP_ABE as abe
import timeit
from analysis import run_analysis

target = abe.ABE()

def test_function():
    (mpk, msk) = target.setup()

num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
execution_times = timeit.repeat("test_function()", setup="from __main__ import test_function", repeat=num_runs, number=1)


run_analysis(execution_times, "myabe setup")