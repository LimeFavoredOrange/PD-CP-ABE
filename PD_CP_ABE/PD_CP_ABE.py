'''
  Author: Xinzhang Chen
  Description: Customized CP-ABE scheme for digital will (data after death) encryption, it supports user collusion resistance and partial decryption. Takes in a list of messages 
  and a set of policy strings, encrypts the messages and returns the cipher texts and the access tree. It encrypts all the messages together by using an integrated access tree,
  during the decryption process, it uses this single access tree to support access control.

  This encryption scheme is a hybrid Ciphertext-Policy Attribute-Based Encryption (CP-ABE) system. The actual content of the information is encrypted using a symmetrically 
  generated encryption key from a pairing-based group. The scheme encrypts the symmetric encryption key itself. Only users who meet the attribute requirements can obtain 
  the symmetric encryption key.

  Based on the paper: "CR-FH-CPABE: Secure File Hierarchy Attribute-Based Encryption Scheme Supporting User Collusion Resistance in Cloud Computing"
  Authors: Yuhan Bai; Kai Fan; Kuan Zhang; Hui Li; Yintang Yang
  Published: 2024
  Paper Link: https://ieeexplore.ieee.org/abstract/document/10416220?casa_token=dUnk3O_XVncAAAAA:ze-IGZhy6w8LVYWk1HBYXNg2pcddw1qcRtRTLWSDBjvgi8_ere51dhZAPXj39IoyZHvpbUBAxbY
'''

from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, pair
from .policy_convertor import policy_convertor
from .tree_builder import tree_builder
from .abe_utils import *

class ABE():
  """
  Class for the CP-ABE scheme, it includes the setup, keygen, encrypt and decrypt functions for the scheme.
  ...

  Attributes
  ----------
  group : PairingGroup
    the bilinear group used for the scheme
  policyConvertor : policy_convertor
    the policy convertor object used for the scheme
  tree_builder : tree_builder
    the tree builder object used for the scheme
  attributeSecretGenerator : attribute_secret_generator
    the attribute secret generator object used for the scheme


  Methods
  -------
  setup():
    Setup function for the scheme (executed at the beginning)
  keygen(mpk, msk, attributes, userID):
    Generate the private access key for the user
  encrypt(mpk, messages, policy_str):
    Encrypt the messages using the policy string
  decrypt(CT, key, ciphers):
    Decrypt the cipher text using the private key
  """

  def __init__(self, groupObj=PairingGroup('SS512'), verbose=False):
    """_summary_

    Args:
      groupObj (PairingGroup, optional): The pairing group that will be used for the scheme. Defaults to PairingGroup('SS512').
      verbose (bool, optional): Debug Mode. Defaults to False.
    """
    self.group = groupObj

    # Access policy parser
    self.policyConvertor = policy_convertor(self.group, verbose=False)

    # Access tree builder
    self.tree_builder = tree_builder(verbose=False)
    
    self.verbose = verbose


  # ========================================================================================================================================================================
  # Helper functions for the scheme
  def h1_hash_from_binary_to_G0(self, binary_string):
    '''
    Hash function from binary string to G0

      Parameters:
        - binary_string: binary string to be hashed

      Returns:
        - G0: hashed value
    '''
    return self.group.hash(binary_string, G1)

  def h2_hash_from_GT_to_ZR(self, element):
    '''
    Hash function from GT to ZR

      Parameters:
        - element: element to be hashed

      Returns:
        - ZR: hashed value
    '''
    element = self.group.serialize(element)
    return self.group.hash(element, ZR)
  
  def h3_hash_from_binary_to_ZR(self, binary_string):
    '''
    Function to hash binary string to ZR

      Parameters:
        - binary_string: binary string to be hashed

      Returns:
        - ZR: hashed value
    '''
    return self.group.hash(binary_string, ZR)

  # ========================================================================================================================================================================
  # Setup function
  def setup(self):
    '''
    Setup function for the scheme
    Only needs to be run once on the broker side while initializing the system
    '''

    # Variables for the bilinear group
    g = self.group.random(G1)
    g.initPP()
    G0 = self.group

    # Random values selected from ZR
    alpha = self.group.random(ZR)
    beta1 = self.group.random(ZR)
    beta2 = self.group.random(ZR)
    beta3 = self.group.random(ZR)
    theta = self.group.random(ZR)

    # f values for MPK (master public key)
    f1 = g ** beta1
    f2 = g ** beta2
    f3 = g ** beta3

    # Mapping value for MPK (master public key)
    e_gg_alpha = pair(g, g) ** alpha

    # MPK construction -> 
    mpk = {'g': g, 'G0': G0, 'f1': f1, 'f2': f2, 'f3': f3, 'e_gg_alpha': e_gg_alpha, 'h1': self.h1_hash_from_binary_to_G0, "h2": self.h2_hash_from_GT_to_ZR}

    # MSK construction -> 
    msk = {'alpha': alpha, 'beta1': beta1, 'beta2': beta2, 'beta3': beta3, 'theta': theta, "h3": self.h3_hash_from_binary_to_ZR}

    return mpk, msk

  # ========================================================================================================================================================================
  # Keygen function
  def keygen(self, mpk, msk, attributes, userID):
    '''
    Keygen function for the CP-ABE scheme

      Parameters:
        - mpk: master public key
        - msk: master secret key
        - attributes: list of attributes for the user
        - userID: information that can be used to uniquely identify the user

      Returns:
        - dict: private key for the user
    '''

    # Change to uppercase for all the attributes
    attributes = [attr.upper() for attr in attributes]

    # Random value for the user
    r_user = self.group.random(ZR)
    w_1 = msk["h3"](userID)

    # For each element in the attribute set, generate a random number
    random_numbers = [self.group.random(ZR) for _ in range(len(attributes))]

    # Compute the private key, use index "user" to represent i
    D_user = mpk['g'] ** ((msk['alpha'] + msk["theta"])/msk["beta1"])
    E_user = mpk['g'] ** ((msk["theta"] + r_user + w_1)/msk["beta2"])
    E_user_tilde = mpk['g'] ** ((r_user + w_1)/msk["beta3"])

    # Create a dictionary to store the keys for the attributes
    attributes_keys = {}

    for i in range(len(attributes)):
      # For every attribute, compute 2 values, use "down" and "up" to distinguish them.
      first_keyName = f"{attributes[i]}_down"
      second_keyName = f"{attributes[i]}_up"

      attributes_keys[first_keyName] = (mpk['g'] ** (r_user + w_1)) * (mpk["h1"](attributes[i]) ** random_numbers[i])
      attributes_keys[second_keyName] = mpk['g'] ** random_numbers[i]

    # Construct the secret key
    sk = {'D_user': D_user, 'E_user': E_user, 'E_user_tilde': E_user_tilde, 'attributes_keys': attributes_keys, "attributes_set": attributes}
    return sk

  # ========================================================================================================================================================================
  # Encryption function
  def encrypt(self, mpk, messages, policy_str):
    """_summary_

    Args:
      mpk (dict): master public key
      messages (list): a list of messages to be encrypted
      policy_str (list): a list of access policies, matching the messages

    Returns:
      cipher_texts (list): a list of cipher texts that encrypt by the symmetric key
      access_tree (object): the access tree constructed for the encryption
    """

    # A list to keep track of the node index, avoid duplicate index
    node_index_list = []

    # Find all the atoms that share the same policy, and combine them
    target = combine_atom_with_policy(messages, policy_str)

    # Get the messages and the corresponding policies
    messages = list(target.values())
    policies = list(target.keys())


    # Random select symmetric keys for each message
    # And use the corresponding key to encrypt the message
    target = symmetric_encryption(self.group, messages)

    # Get a list of symmetric keys
    keys = target["keys"]

    # Get a list of cipher texts
    cipher_texts = target["cipher_texts"]

    # Generate the attribute set and the attribute node collection
    attributes_set, attribute_nodes = self.policyConvertor.createAttribute_node(policy_str, node_index_list)
    
    # Generate the atom node collection
    atom_nodes = self.policyConvertor.generate_atom_nodes(len(keys), policies, node_index_list)

    # Generate the link node collection
    link_nodes = self.policyConvertor.generate_link_nodes(atom_nodes, attribute_nodes, node_index_list)

    # Construct the access tree
    access_tree = self.tree_builder.build_tree_link(atom_nodes, attribute_nodes, link_nodes, attributes_set)

    # Setup the cryptographic parameters for the atom nodes
    access_tree.setup_atome_nodes_link(self.group, mpk, keys, self.group.random)

    return cipher_texts, access_tree

  # Decryption function
  def decrypt(self, CT, key, ciphers):
    """_summary_

    Args:
      CT (object): the cipher encrypted object returned from the encrypt function
      key (dict): the private access key for the user
      ciphers (list): a list of cipher texts that encrypt by the symmetric key

    Returns:
        decrypted_result (dict): a dictionary that contains the decrypted result
    """

    # Construct a structure to keep track of the decryption result
    decryption_result = {}
    for node in CT.atom_nodes.values():
      decryption_result[node.id] = {
        "policy": node.policy,
        "Decryptable": False,
      }

    decrypted_points = {}
    for atom in CT.atom_nodes.values():
      # For each atom node, call the decrypt function, it will walk down the tree and try to decrypt the value
      (status, value) = atom.decrypt(key, self.group, f"Atom{atom.id}", decrypted_points)

      # If the status is true, then the decryption is successful (Eligible to view the content of the atom)
      if status:
        C_li = atom.C_li
        C_li_tile = atom.C_li_tile
        C_li_double_tile = atom.C_li_double_tile
        C_li_triple_tile = atom.C_li_triple_tile


        temp1 = pair(C_li_tile, key["D_user"])
        temp2 = pair(C_li_triple_tile, key["E_user_tilde"])
        temp3 = pair(C_li_double_tile, key["E_user"])
        check = (temp1 * temp2 * value) / temp3

        final = (C_li / check)

        # Update the decryption result
        ans = symmetric_decryption(final, ciphers[int(atom.id) - 1]).decode('utf-8')
        decryption_result[atom.id]["Decryptable"] = ans.split("lala")
    return decryption_result