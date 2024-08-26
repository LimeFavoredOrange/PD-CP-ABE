import pytest
import sys
import os
import pickle
from charm.toolbox.pairinggroup import GT

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path: sys.path.append(project_root)


from PD_CP_ABE import PD_CP_ABE, abe_utils


@pytest.fixture
def abe_instance():
    target = PD_CP_ABE.ABE()
    mpk, msk = target.setup()
    return target, mpk, msk

# Serialize testing

def test_serialize_key(abe_instance):
    target, mpk, msk = abe_instance
    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    expected_keys = ["D_user", "E_user", "E_user_tilde", "attributes_keys"]
    serialized_key = abe_utils.serializeKey(target.group, key)
    # Check the returned value from the function is a dict
    assert isinstance(serialized_key, dict)

    # Check the structure of the serialized key
    assert all(key in serialized_key for key in expected_keys)
    assert isinstance(serialized_key["D_user"], bytes)
    assert isinstance(serialized_key["E_user"], bytes)
    assert isinstance(serialized_key["E_user_tilde"], bytes)
    assert all(isinstance(value, bytes) for value in serialized_key["attributes_keys"].values())
    assert isinstance(serialized_key["attributes_set"], list)


def test_deserialize_key(abe_instance):
    target, mpk, msk = abe_instance
    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    serialized_key = abe_utils.serializeKey(target.group, key)
    deserialized_key = abe_utils.deserializeKey(target.group, serialized_key)
    assert isinstance(deserialized_key, dict)
    assert all(key in deserialized_key for key in serialized_key.keys())
    # Check the type is the same as the type of the original key
    assert isinstance(deserialized_key["D_user"], type(key["D_user"]))
    assert isinstance(deserialized_key["E_user"], type(key["E_user"]))
    assert isinstance(deserialized_key["E_user_tilde"], type(key["E_user_tilde"]))
    assert all(isinstance(value, type(v)) for value, v in zip(deserialized_key["attributes_keys"].values(), key["attributes_keys"].values()))
    assert isinstance(deserialized_key["attributes_set"], list)
    assert deserialized_key["attributes_set"] == key["attributes_set"]

def test_export_key_to_file(abe_instance):
    target, mpk, msk = abe_instance
    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    serialized_key = abe_utils.serializeKey(target.group, key)
    abe_utils.export_key_to_file(target.group, "key_test", serialized_key)
    # Check the file "key_test.pkl" exists
    assert os.path.exists("key_test.pkl")
    assert os.path.isfile("key_test.pkl")
    # Check the content of the file
    with open("key_test.pkl", "rb") as file:
        data = file.read()
    assert pickle.loads(data) == serialized_key

def test_read_key_from_file(abe_instance):
    target, mpk, msk = abe_instance
    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    serialized_key = abe_utils.serializeKey(target.group, key)
    abe_utils.export_key_to_file(target.group, "key_test", serialized_key)
    deserialized_key = abe_utils.read_key_from_file(target.group, "key_test.pkl")
    assert isinstance(deserialized_key, dict)
    assert all(key in deserialized_key for key in serialized_key.keys())
    # Check the type is the same as the type of the original key
    assert isinstance(deserialized_key["D_user"], type(key["D_user"]))
    assert isinstance(deserialized_key["E_user"], type(key["E_user"]))
    assert isinstance(deserialized_key["E_user_tilde"], type(key["E_user_tilde"]))
    assert all(isinstance(value, type(v)) for value, v in zip(deserialized_key["attributes_keys"].values(), key["attributes_keys"].values()))
    assert isinstance(deserialized_key["attributes_set"], list)
    assert deserialized_key["attributes_set"] == key["attributes_set"]
    # Check the file "key_test.pkl" exists
    assert os.path.exists("key_test.pkl")
    assert os.path.isfile("key_test.pkl")
    # Check the content of the file
    with open("key_test.pkl", "rb") as file:
        data = file.read()
    assert pickle.loads(data) == serialized_key
    # Remove the file
    os.remove("key_test.pkl")


def test_export_ciphers_to_file(abe_instance):
    # Encrypt the message
    target, mpk, msk = abe_instance
    messages = ["Hello", "World", "!"]
    access_policies = ["(A and B)", "(A or B)", "(A or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    abe_utils.export_ciphers_to_file(target.group, ciphers, access_tree, "ciphers_test")

    # Check the folder "ciphers_test" exists
    assert os.path.exists("ciphers_test")
    assert os.path.isdir("ciphers_test")
    # Check the file "ciphers_test/data.pkl" exists
    assert os.path.exists("ciphers_test/data.pkl")
    assert os.path.isfile("ciphers_test/data.pkl")

    # Check the file "ciphers_test/ciphers.pkl" exists
    assert os.path.exists("ciphers_test/ciphers.pkl")
    assert os.path.isfile("ciphers_test/ciphers.pkl")



def test_read_ciphers(abe_instance):
    # Read from the folder
    target, mpk, msk = abe_instance
    ciphers, access_tree = abe_utils.read_ciphers(target.group, "ciphers_test")
    assert isinstance(ciphers, list)
    assert len(access_tree.atom_nodes) == 3
    assert len(access_tree.attribute_nodes) == 3
    assert access_tree.attributes_set == {"A", "B", "C"}

    # Remove the folder
    os.remove("ciphers_test/data.pkl")
    os.remove("ciphers_test/ciphers.pkl")
    os.rmdir("ciphers_test")




