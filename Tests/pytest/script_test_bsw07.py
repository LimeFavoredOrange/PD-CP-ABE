import json
from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.adapters.abenc_adapt_hybrid import HybridABEnc


def setup(test_input_path):
    group = PairingGroup('SS512')
    cpabe = CPabe_BSW07(group)
    hyb_abe = HybridABEnc(cpabe, group)
    (master_public_key, master_key) = hyb_abe.setup()

    with open(f"{test_input_path}/twitter_responses_1500.json", "r") as file:
        tweets = json.load(file)
    return master_public_key, master_key, tweets, hyb_abe

def test(duplicate=False):
    test_input_path = "../inputs"
    test_file_path = f"{test_input_path}/twitter_access_policies_duplicate_1500.json" if duplicate else f"{test_input_path}/twitter_access_policies_1500.json"
    master_public_key, master_key, tweets, hyb_abe = setup(test_input_path)

    with open(test_file_path, "r") as file:
        access_policies = json.load(file)

    result = {}
    for item in tweets:
        item = json.loads(item)
        id = item["data"]["id"]
        result[id] = False

    attributes = ["Trusted", "Senior", "Student", "Engineer", "Visitor", "Remote", "Regular", "Local", "VIP", "Manager"]
    attributes_upper = [item.upper() for item in attributes]


    secret_key = hyb_abe.keygen(master_public_key, master_key, attributes_upper)

    for i in range(0, len(tweets)):
        cipher_text = hyb_abe.encrypt(master_public_key, tweets[i], access_policies[i])
        try:
            decrypted_msg = hyb_abe.decrypt(master_public_key, secret_key, cipher_text)
            id = json.loads(decrypted_msg.decode())["data"]["id"]
            result[id] = True
        except:
            pass
    return result, len(tweets), sum(result.values())

if __name__ == "__main__":
    result, total, decrypted = test()
    print(result)
    print(total)
    print(decrypted)