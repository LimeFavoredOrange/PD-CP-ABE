import os
import sys


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path: sys.path.append(project_root)

from PD_CP_ABE import PD_CP_ABE
import json

def setup(test_input_path):
  target = PD_CP_ABE.ABE()
  (mpk, msk) = target.setup()

  with open(f"{test_input_path}/twitter_responses_1500.json", "r") as file:
    tweets = json.load(file)

  return  mpk, msk, tweets, target


def test(duplicate=False):
  test_input_path = "../inputs"
  test_file_path = f"{test_input_path}/twitter_access_policies_duplicate_1500.json" if duplicate else f"{test_input_path}/twitter_access_policies_1500.json"
  mpk, msk, tweets, target = setup(test_input_path)

  with open(test_file_path, "r") as file:
    access_policies = json.load(file)
  
  result = {}

  for item in tweets:
    item = json.loads(item)
    id = item["data"]["id"]
    result[id] = False

  attributes = ["Trusted", "Senior", "Student", "Engineer", "Visitor", "Remote", "Regular", "Local", "VIP", "Manager"]

  key = target.keygen(mpk, msk, attributes, "Alice")

  cipher_text, access_tree = target.encrypt(mpk, tweets, access_policies)
  try:
    decrypted_msg = target.decrypt(access_tree, key, cipher_text)

    for key, value in decrypted_msg.items():
      if value["Decryptable"] != False:
        target_list = value["Decryptable"]
        for item in target_list:
          id = json.loads(item)["data"]["id"]
          result[id] = True
  except Exception as e:
    pass
  
  return result, len(tweets),sum(result.values())

if __name__ == "__main__":
  result, total, decrypted = test()
  print(result)
  print(total)
  print(decrypted)



