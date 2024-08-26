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
# Test for single atom -> and case

def test_decrypt_single_simple_atom_and_success(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["(A and B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Hello']}}

def test_decrypt_single_simple_atom_and_fail(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["(A and B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}}
# ==================================================================================================================================================================


# ==================================================================================================================================================================
# Test for single atom -> or case

def test_decrypt_single_simple_atom_or_success(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["(A or B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}}

def test_decrypt_single_simple_atom_or_fail(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["(A or B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}}
# ==================================================================================================================================================================

# ==================================================================================================================================================================
def test_decrypt_single_atom_with_conenction_and_success(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["((A and B) and C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': ['Hello']}}

def test_decrypt_single_atom_with_connection_and_fail(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["((A and B) and C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}}

def test_decrypt_single_atom_with_conenction_or_success(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["((A or B) or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A or B) or C)', 'Decryptable': ['Hello']}}

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A or B) or C)', 'Decryptable': ['Hello']}}


    access_policies = ["((A and B) or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) or C)', 'Decryptable': ['Hello']}}

    key = target.keygen(mpk, msk, ["A", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) or C)', 'Decryptable': ['Hello']}}

    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) or C)', 'Decryptable': ['Hello']}}


    access_policies = ["(((A and B) or C) or B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(((A and B) or C) or B)', 'Decryptable': ['Hello']}}

    key = target.keygen(mpk, msk, ["A", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(((A and B) or C) or B)', 'Decryptable': ['Hello']}}

    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(((A and B) or C) or B)', 'Decryptable': ['Hello']}}
