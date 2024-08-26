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


# Test for and gate with duplicate attributes -> success
def test_and_duplicate_attribute_success(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A and A)", "((A and A) and A)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and A)', 'Decryptable': ['Hello']}, '2': {'policy': '((A and A) and A)', 'Decryptable': ['World']}}

    access_policies = ["(A and A)", "((C or (((A and A) and A) or B)) or B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and A)', 'Decryptable': ['Hello']}, '2': {'policy': '((C or (((A and A) and A) or B)) or B)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and A)', 'Decryptable': False}, '2': {'policy': '((C or (((A and A) and A) or B)) or B)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and A)', 'Decryptable': ['Hello']}, '2': {'policy': '((C or (((A and A) and A) or B)) or B)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and A)', 'Decryptable': False}, '2': {'policy': '((C or (((A and A) and A) or B)) or B)', 'Decryptable': ['World']}}

# Test for and gate with duplicate attributes -> fail
def test_and_duplicate_attribute_fail(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["(A and A)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and A)', 'Decryptable': False}}


# Test for or gate with duplicate attributes -> success
def test_or_duplicate_attribute_success(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["(A or A)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or A)', 'Decryptable': ['Hello']}}

# Test for or gate with duplicate attributes -> fail
def test_or_duplicate_attribute_fail(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello"]
    access_policies = ["(A or A)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or A)', 'Decryptable': False}}
