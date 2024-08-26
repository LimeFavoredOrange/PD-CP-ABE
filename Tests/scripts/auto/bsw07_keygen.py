import timeit
import sys
from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from analysis import run_analysis


group = PairingGroup('SS512')
cpabe = CPabe_BSW07(group)
hyb_abe = HybridABEnc(cpabe, group)
(master_public_key, master_key) = hyb_abe.setup()

number_of_attribure = int(sys.argv[2]) if len(sys.argv) > 2 else 6

# Generage this number of attribures
target_attribute = [str(i) for i in range(number_of_attribure)]


def test_function():
    attributes = target_attribute
    secret_key = hyb_abe.keygen(master_public_key, master_key, attributes)

num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
execution_times = timeit.repeat("test_function()", setup="from __main__ import test_function", repeat=num_runs, number=1)

# Compute statistics
run_analysis(execution_times, f"bsw07 keygen {number_of_attribure} attributes")