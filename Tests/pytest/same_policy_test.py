import pytest
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path: sys.path.append(project_root)

from PD_CP_ABE import PD_CP_ABE


@pytest.fixture
def abe_instance():
    target = PD_CP_ABE.ABE()
    mpk, msk = target.setup()
    return target, mpk, msk

# ==================================================================================================================================================================
# Test for the same policy, two atoms sharing the same policy (and gate)
def test_decrypt_share_same_policy_and(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A and B)", "(A and B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Hello', 'World']}}

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}}


# Test for the same policy, two/more atoms sharing the same policy but different order (and gate)
def test_decrypt_share_same_policy_different_order_and(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A and B)", "(B and A)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Hello']}, '2': {'policy': '(B and A)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(B and A)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(B and A)', 'Decryptable': False}}


    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(B and A)', 'Decryptable': False}}


    messages = ["Hello", "World", "Hello World"]
    access_policies = ["(A and B)", "(B and A)", "(B and A)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Hello']}, '2': {'policy': '(B and A)', 'Decryptable': ['World', 'Hello World']}}


# Test for the same policy, two atoms sharing the same policy (or gate)
def test_decrypt_share_same_policy_or(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A or B)", "(A or B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello', "World"]}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello', "World"]}}

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello', "World"]}}

    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}}

# Test for the same policy, two/more atoms sharing the same policy but different order (or gate)
def test_decrypt_share_same_policy_different_order_or(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A or B)", "(B or A)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(B or A)', 'Decryptable': ["World"]}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(B or A)', 'Decryptable': ["World"]}}


    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(B or A)', 'Decryptable': ["World"]}}


    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}, '2': {'policy': '(B or A)', 'Decryptable': False}}


    messages = ["Hello", "World", "Hello World"]
    access_policies = ["(A or B)", "(B or A)", "(B or A)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(B or A)', 'Decryptable': ["World", "Hello World"]}}


# Test for the same policy, many atoms sharing the same policy (and gate)
def test_decrypt_multiple_no_share_same_policy_and(abe_instance):
    target, mpk, msk = abe_instance
    # Test for 8 messages for this case
    messages = ["Text1", "Text2", "Text3", "Text4", "Text5", "Text6", "Text7", "Text8"]
    access_policies = ["(A and B)", "(C and D)", "(A and B)", "(C and D)", "(A and B)", "(C and D)", "(C and D)", "(A and B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Text1', "Text3", "Text5", "Text8"]}, '2': {'policy': '(C and D)', 'Decryptable': ['Text2', "Text4", "Text6", "Text7"]}}

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Text1', "Text3", "Text5", "Text8"]}, '2': {'policy': '(C and D)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["C", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(C and D)', 'Decryptable': ['Text2', "Text4", "Text6", "Text7"]}}

    key = target.keygen(mpk, msk, ["A", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(C and D)', 'Decryptable': False}}


# Test for the same policy, many atoms sharing the same policy (or gate)
def test_decrypt_multiple_phase_node_or_no_share_same_policy(abe_instance):
    target, mpk, msk = abe_instance
    # Test for 8 messages for this case
    messages = ["Text1", "Text2", "Text3", "Text4", "Text5", "Text6", "Text7", "Text8"]
    access_policies = ["(A or B)", "(C or D)", "(A or B)", "(C or D)", "(A or B)", "(C or D)", "(C or D)", "(A or B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Text1', "Text3", "Text5", "Text8"]}, '2': {'policy': '(C or D)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Text1', "Text3", "Text5", "Text8"]}, '2': {'policy': '(C or D)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Text1', "Text3", "Text5", "Text8"]}, '2': {'policy': '(C or D)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["C", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}, '2': {'policy': '(C or D)', 'Decryptable': ['Text2', "Text4", "Text6", "Text7"]}}

    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}, '2': {'policy': '(C or D)', 'Decryptable': ['Text2', "Text4", "Text6", "Text7"]}}

    key = target.keygen(mpk, msk, ["D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}, '2': {'policy': '(C or D)', 'Decryptable': ['Text2', "Text4", "Text6", "Text7"]}}






