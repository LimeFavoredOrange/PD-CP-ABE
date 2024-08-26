import json
import timeit
import sys
from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from analysis import run_analysis



test_input_path = "../../inputs"


with open (f"{test_input_path}/twitter_responses_1500.json") as file:
    messages = json.load(file)

with open(f"{test_input_path}/twitter_access_policies_1500.json") as file:
    policies = json.load(file)

number_of_atoms = int(sys.argv[2]) if len(sys.argv) > 2 else 5
group = PairingGroup('SS512')
cpabe = CPabe_BSW07(group)
hyb_abe = HybridABEnc(cpabe, group)
(master_public_key, master_key) = hyb_abe.setup()

attributes = ["A", "B", "C", "E", "G","K"]
secret_key = hyb_abe.keygen(master_public_key, master_key, attributes)
access_policies = policies[:number_of_atoms]

def test_function():
    for i in range(0, number_of_atoms):
        cipher_text = hyb_abe.encrypt(master_public_key, messages[i], access_policies[i])

num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
execution_times = timeit.repeat("test_function()", setup="from __main__ import test_function", repeat=num_runs, number=1)

# Compute statistics
run_analysis(execution_times, f"bsw07 encrytpion {number_of_atoms} atoms")