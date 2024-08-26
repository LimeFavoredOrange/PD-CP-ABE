import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', ".."))
if project_root not in sys.path: sys.path.append(project_root)


from PD_CP_ABE import PD_CP_ABE as abe
import timeit
import json
from analysis import run_analysis

test_input_path = "../../inputs"

data = None
policies = None
with open(f"{test_input_path}/twitter_responses_1500.json") as file:
    data = json.load(file)

with open(f"{test_input_path}/twitter_access_policies_duplicate_1500.json") as file:
    policies = json.load(file)


number_of_atom = int(sys.argv[2]) if len(sys.argv) > 2 else 6

target = abe.ABE()
(mpk, msk) = target.setup()
key = target.keygen(mpk, msk, ["Trusted", "Senior", "Student", "Engineer", "Visitor", "Remote", "Regular", "Local", "VIP", "Manager"], "Alice")
messages = data[:number_of_atom]
access_policies = policies[:number_of_atom]

def test_function():
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)


num_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
execution_times = timeit.repeat("test_function()", setup="from __main__ import test_function", repeat=num_runs, number=1)

run_analysis(execution_times, f"myabe encryption {number_of_atom} atoms")
