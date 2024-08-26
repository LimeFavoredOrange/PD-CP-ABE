from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.abenc.abenc_bsw07 import CPabe_BSW07
from charm.adapters.abenc_adapt_hybrid import HybridABEnc


group = PairingGroup('SS512')
cpabe = CPabe_BSW07(group)
hyb_abe = HybridABEnc(cpabe, group)
(master_public_key, master_key) = hyb_abe.setup()

attributes = ["Trusted", "Senior", "Student", "Engineer", "Visitor", "Remote", "Regular", "Local", "VIP", "Manager"]
attributes_temp  = [item.upper() for item in attributes]

secret_key = hyb_abe.keygen(master_public_key, master_key, attributes_temp)

messages = "Hello"
policy = "(VIP and VIP)"


cipher_text = hyb_abe.encrypt(master_public_key, messages, policy)
try:
    decrypted_msg = hyb_abe.decrypt(master_public_key, secret_key, cipher_text)
    print(decrypted_msg)
except Exception as e:
    print(e)
    pass