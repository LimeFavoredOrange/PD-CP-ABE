import pytest
import sys
import os
from charm.toolbox.pairinggroup import GT

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path: sys.path.append(project_root)


from PD_CP_ABE import PD_CP_ABE


@pytest.fixture
def abe_instance():
    target = PD_CP_ABE.ABE()
    mpk, msk = target.setup()
    return target, mpk, msk

# Scheme basic testing

# Test the setup function
def test_setup(abe_instance):
    target, mpk, msk = abe_instance
    assert mpk is not None
    assert msk is not None
    assert isinstance(mpk, dict)
    assert isinstance(msk, dict)

# Test the structure of the mpk
def test_mpk_structure(abe_instance):
    target, mpk, _ = abe_instance
    assert isinstance(mpk, dict)
    expected_keys = {'g', 'G0', 'f1', 'f2', 'f3', 'e_gg_alpha', 'h1', 'h2'}
    assert set(mpk.keys()) == expected_keys

    # Test the 'h2' function, hash function from GT to ZR
    # Generate a random element in GT
    element = target.group.random(GT)
    hash1 = mpk['h2'](element)
    hash2 = mpk['h2'](element)
    assert hash1 == hash2

# Test the structure of the msk
def test_msk_structure(abe_instance):
    target, _, msk = abe_instance
    assert isinstance(msk, dict)
    expected_keys = {'alpha', 'beta1', 'beta2', 'beta3', 'theta', 'h3'}
    assert set(msk.keys()) == expected_keys

# Test the generation of the key and the structure of the key
def test_keygen(abe_instance):
    target, mpk, msk = abe_instance
    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    assert key is not None
    assert isinstance(key, dict)
    assert set(key.keys()) == {"D_user", "E_user", "E_user_tilde", "attributes_keys", "attributes_set" }
    assert key["attributes_set"] == ["A", "B", "C"]
    assert len(key["attributes_keys"]) == 6

# Test the encryption function
def test_encrypt(abe_instance):
    target, mpk, _ = abe_instance
    messages = ["Hello", "World", "HEllo"]
    access_policies = ["(A and B)", "(A or B)", "(A or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    assert ciphers is not None
    assert access_tree is not None
    assert len(ciphers) == len(messages)
    assert len(ciphers) == len(access_policies)
    assert len(access_tree.atom_nodes) == 3 and len(access_tree.attribute_nodes) == 3
    assert access_tree.attributes_set == {"A", "B", "C"}

# Test the decryption function
def test_decrypt(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World", "HEllo"]
    access_policies = ["(A and B)", "(A or B)", "(A or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    decrypted_msg = target.decrypt(access_tree, key, ciphers)
    assert decrypted_msg is not None
    assert isinstance(decrypted_msg, dict)
    assert len(decrypted_msg) == len(messages)
    for key, value in decrypted_msg.items():
        assert value["Decryptable"] != False