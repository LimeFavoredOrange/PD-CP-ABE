"""
This file contains the utility functions for the ABE scheme

Functions:
    - symmetric_encryption(group, M_list)
    - symmetric_decryption(key, cipher_text)
    - serializeKey(group, key)
    - deserializeKey(group, data)
    - export_key_to_file(group, filename, key)
    - read_key_from_file(group, filename)
    - serialize(group, access_tree)
    - deserialize(group, access_tree)
    - export_ciphers_to_file(group, ciphers, access_tree, folder_name)
    - read_ciphers(group, folder_path)
    - combine_atom_with_policy(atoms, policies)
"""

from charm.toolbox.pairinggroup import GT
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import hashPair as sha2
from charm.core.engine.util import objectToBytes, bytesToObject
import pickle
import os


# ====================================================================
# Symmetric key encryption functions
def symmetric_encryption(group, M_list):
  """Encrypts a list of messages using symmetric key encryption

  Args:
      group (PairingGroup): The pairing group to use
      M_list (list): The list of messages to encrypt

  Returns:
      encrypted_components (dict): A dictionary containing the encrypted
  """

  encrypted_components = {"keys": [], "cipher_texts": []}
  for message in M_list:
    # Choose a random key
    key = group.random(GT)

    # Encrypt the message
    cipher = AuthenticatedCryptoAbstraction(sha2(key))
    encrypted_components["keys"].append(key)
    encrypted_components['cipher_texts'].append(cipher.encrypt('lala'.join(message)))
  return encrypted_components

# ====================================================================
# Symmetric key decryption functions
def symmetric_decryption(key, cipher_text):
  """Decrypts a cipher text using symmetric key encryption

  Args:
    key (GT): The key to use for decryption
    cipher_text (bytes): The cipher text to decrypt

  Returns:
    data: bytes: The decrypted
  """

  cipher = AuthenticatedCryptoAbstraction(sha2(key))
  return cipher.decrypt(cipher_text)

# ====================================================================
# Key serialize and deserialize functions
def serializeKey(group, key):
  """ Serializes the key to bytes

  Args:
      group (PairingGroup): The pairing group to use
      key (dict): The key to serialize

  Returns:
      serialized_key (dict): The serialized key
  """

  key["D_user"] = objectToBytes(key["D_user"], group)
  key["E_user"] = objectToBytes(key["E_user"], group)
  key["E_user_tilde"] = objectToBytes(key["E_user_tilde"], group)

  for k, v in key["attributes_keys"].items():
    key["attributes_keys"][k] = objectToBytes(v, group)

  return key

def deserializeKey(group, data):
  """Deserializes the key from bytes

  Args:
    group (PairingGroup): The pairing group to use
    data (dict): The data to deserialize

  Returns:
    key (dict): The deserialized key
  """

  data["D_user"] = bytesToObject(data["D_user"], group)
  data["E_user"] = bytesToObject(data["E_user"], group)
  data["E_user_tilde"] = bytesToObject(data["E_user_tilde"], group)
  for k, v in data["attributes_keys"].items():
    data["attributes_keys"][k] = bytesToObject(v, group)

  return data

# ====================================================================
# System key export and import functions
def export_key_to_file(group, filename, key):
  """Exports the key to a file

  Args:
    group (PairingGroup): The pairing group to use
    filename (str): The name of the file to export the key to
    key (dict): The key to export
  
  Returns:
    None
  """
  key = serializeKey(group, key)
  filename = filename + ".pkl"
  with open(filename, "wb") as file:
    pickle.dump(key, file)

def read_key_from_file(group, filename):
  """Reads the key from a file

  Args:
      group (PairingGroup): The pairing group to use
      filename (str): The name of the file to read the key from

  Returns:
      key (dict): The key read from the file
  """
  filename = filename + ".pkl"
  with open(filename, "rb") as file:
    data = pickle.load(file)
  return deserializeKey(group, data)


# ====================================================================
# Serialize and deserialize the access tree
def serialize(group, access_tree):
  """Serializes the access tree to bytes

  Args:
    group (PairingGroup): The pairing group to use
    access_tree (AccessTree): The access tree to serialize

  Returns:
    access_tree (AccessTree): The serialized access tree
  """
  for node in access_tree.atom_nodes.values():
    node.serialize(group)
  return access_tree

def deserialize(group, access_tree):
  """Function to deserialize the access tree

  Args:
      group (PairingGroup): The pairing group to use
      access_tree (AccessTree): The access tree to deserialize

  Returns:
      access_tree (AccessTree): The deserialized access tree
  """
  for node in access_tree.atom_nodes.values():
    node.deserialize(group)
  return access_tree

# ====================================================================
# Export and import the ciphers to a file
def export_ciphers_to_file(group, ciphers, access_tree, folder_name):
  """Function to export the ciphers to a file

  Args:
    group (PairingGroup): The pairing group to use
    ciphers (list): A list of ciphers to export
    access_tree (AccessTree): The access tree to export
    folder_name (str): The name of the folder to export the ciphers to

  Returns:
    None
  """
  folder_path = folder_name
    
  # Check the folder is already exist or not
  if not os.path.exists(folder_path):
    os.makedirs(folder_path)
  
  # Create the file paths
  data_path = os.path.join(folder_path, "data.pkl")
  cipher_path = os.path.join(folder_path, "ciphers.pkl")

  # Write the ciphers to the file
  with open(data_path, 'wb') as file:
    pickle.dump(ciphers, file)
  
  with open(cipher_path, "wb") as file:
    pickle.dump(serialize(group, access_tree), file)

def read_ciphers(group, folder_path):
  """Function to read the ciphers from a file

  Args:
      group (PairingGroup): The pairing group to use
      folder_path (str): The name of the folder to read the ciphers from

  Returns:
      data_object(dict): The ciphers read from the file
      cipher_object (AccessTree): The AccessTree read from the file
  """

  data_path = os.path.join(folder_path, "data.pkl")
  cipher_path = os.path.join(folder_path, "ciphers.pkl")

  data_object = None
  cipher_object = None

  with open(data_path, "rb") as file:
    data_object = pickle.load(file)

  with open(cipher_path, "rb") as file:
    cipher_object = deserialize(group, pickle.load(file))
  
  return data_object, cipher_object

# ====================================================================
# Helper function to map each atom with the corresponding access policy
def combine_atom_with_policy(atoms, policies):
  """Function to combine the atoms with the corresponding access policy

  Args:
      atoms (list): A list of messages
      policies (list): A list of access policies

  Returns:
      grouped_messages(dict): A dictionary containing the combined messages
  """
  # Create a empty dictionary to store the combined result
  grouped_messages = {}

  for message, pol in zip(atoms, policies):
    # If the policy is already in the dictionary, append the message to the corresponding list
    if pol in grouped_messages:
      grouped_messages[pol].append(message)
    # Otherwise, create a new list and add the message to it
    else:
      grouped_messages[pol] = [message]
  return grouped_messages

