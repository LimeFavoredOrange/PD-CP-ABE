import sys
import os
import json

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path: sys.path.append(project_root)

from PD_CP_ABE import PD_CP_ABE

target = PD_CP_ABE.ABE()


# Every time we run this code, we will get a different key
(mpk, msk) = target.setup()


attributes = ["A", "B"]
key = target.keygen(mpk, msk, attributes, "Alice")

messages = ["Hello"]
policy = ["(A and B)"]

cipher_text, access_tree = target.encrypt(mpk, messages, policy)
try:
  decrypted_msg = target.decrypt(access_tree, key, cipher_text)
  print(decrypted_msg)
except:
    pass


