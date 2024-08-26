'''
    This is the example program for the Partially Decryptable Ciphertext Policy Attribute-Based Encryption Scheme (PD-CP-ABE)
    You can run this program to see how the PD-CP-ABE scheme works.
    Including the following steps:
    1. Setup
    2. Key Generation
    3. Encryption
    4. Decryption
'''

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path: sys.path.append(project_root)

from PD_CP_ABE import PD_CP_ABE, abe_utils

# Please change the following data according to your requirements

# The variable is used to represent the user's attributes
user_attributes = ["A", "B"]

# The variable is used to represent the user's ID, which can be uniquely identified by the system
# I use the user's name as the user's ID in this example, to make it easier to understand
user_name = "Alice"

# This is the list of messages that you want to encrypt
messages = ["Hello", "World", "Hello World"]

# This is the access policy that you want to set for the ciphertext
# The access policy is a string that represents the logical relationship between the attributes
# You can use the following operators in the access policy:
#   - 'and' : Logical AND
#   - 'or' : Logical OR
access_policies = ["(A and B)", "(A or B)", "(A and C)"]


def is_default_setting():
    """This function is used to determine whether the default setting is used
    If the default setting is used, the default access key can decrypt the first and second ciphertexts, but not the third
    """
    return user_attributes == ["A", "B"] and user_name == "Alice" and messages == ["Hello", "World", "Hello World"] and access_policies == ["(A and B)", "(A or B)", "(A and C)"]

def main():
    # Initialize the PD-CP-ABE scheme
    target = PD_CP_ABE.ABE()

    # Setup the scheme
    mpk, msk = target.setup()

    # Generate the key for the user
    key = target.keygen(mpk, msk, user_attributes, user_name)

    # You can export the access key and store it in a file
    abe_utils.export_key_to_file(target.group, "key", key)

    # Encrypt the message
    ct, data = target.encrypt(mpk, messages, access_policies)

    # Save the ciphertext to a file
    abe_utils.export_ciphers_to_file(target.group, ct, data, "ciphers")

    # Read the key from the file
    key = abe_utils.read_key_from_file(target.group, "key")

    # Read the ciphertext from the file
    ct, data = abe_utils.read_ciphers(target.group, "ciphers")

    # Decrypt the ciphertext using the key
    result = target.decrypt(data, key, ct)


    if is_default_setting():
        # Based on the default attributes set, the default access key
        # can decrypt the first and second ciphertexts, but not the third
        # Note: If you change the default setting, the following results may be different
        assert result['1']['Decryptable'] != False
        assert result['1']['Decryptable'][0] == messages[0]
        assert result['2']['Decryptable'] != False
        assert result['2']['Decryptable'][0] == messages[1]
        assert result['3']['Decryptable'] == False

    print("Decryption result: ")
    for value in result.values():
        print(value)

if __name__ == "__main__":
    main()