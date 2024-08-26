import json
import sys
import timeit
from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from analysis import run_analysis


test_input_path = "../../inputs"


with open (f"{test_input_path}/twitter_responses_1500.json") as file:
    messages = json.load(file)


with open(f"{test_input_path}/twitter_access_policies_1500.json") as file:
    policies = json.load(file)

number_of_atoms = int(sys.argv[2]) if len(sys.argv) > 2 else 6

group = PairingGroup('SS512')
cpabe = CPabe_BSW07(group)
hyb_abe = HybridABEnc(cpabe, group)
(master_public_key, master_key) = hyb_abe.setup()

attributes = ["Trusted", "Senior", "Student", "Engineer", "Visitor", "Remote", "Regular", "Local", "VIP", "Manager"]
secret_key = hyb_abe.keygen(master_public_key, master_key, attributes)
ciphers = []
access_policies = policies[:number_of_atoms]
for i in range(0, number_of_atoms):
    cipher_text = hyb_abe.encrypt(master_public_key, messages[i], access_policies[i])
    ciphers.append(cipher_text)

def test_function():
    for i in range(0, number_of_atoms):
        try :
            hyb_abe.decrypt(master_public_key, secret_key, ciphers[i])
        except Exception as e:
            # print(e)
            continue

num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
execution_times = timeit.repeat("test_function()", setup="from __main__ import test_function", repeat=num_runs, number=1)

# Compute statistics
run_analysis(execution_times, f"bsw07 decryption {number_of_atoms} atoms")