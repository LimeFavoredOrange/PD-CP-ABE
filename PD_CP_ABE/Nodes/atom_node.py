from charm.core.engine.util import objectToBytes, bytesToObject


class AtomNode:
  """
    A class used to represent an Atom node

    Attributes
    ----------
    id : str
      a unique identifier for the node
    policy : str
      the policy of the node
    type : str
      the type of the node
    index : int
      the index of the node
    childNode : Node
      the child node of the node
    C_li : object
      the C_li value of the node
    C_li_tile : object
      the C_li_tile value of the node
    C_li_double_tile : object
      the C_li_double_tile value of the node
    C_li_triple_tile : object
      the C_li_triple_tile value of the node

    Methods
    -------
    set_chileNode(childNode)
      Set the child node of the node
    set_C_li(C_li)
      Set the C_li value of the node
    set_C_li_tile(C_li_tile)
      Set the C_li_tile value of the node
    set_C_li_double_tile(C_li_double_tile)
      Set the C_li_double_tile value of the node
    set_C_li_triple_tile(C_li_triple_tile)
      Set the C_li_triple_tile value of the node
    propagate_values(group, computed_points, mpk, secret, title)
      Propagate the values of the node
    decrypt(key, group, title, decrypted_points)
      Decrypt the node
    getNodeType()
      Get the type of the node
    serialize(group)
      Serialize the node
    deserialize(group)
      Deserialize the node
    """
  

  # The init function of the AtomNode class
  def __init__(self, index, value, policy):		
    self.id = value
    self.policy = policy
    self.type = "Atom"

    self.index = index
    self.childNode = None

    self.C_li = None
    self.C_li_tile = None
    self.C_li_double_tile = None
    self.C_li_triple_tile = None

  def set_chileNode(self, childNode):
    self.childNode = childNode
  
  def set_C_li(self, C_li):
    self.C_li = C_li
  
  def set_C_li_tile(self, C_li_tile):
    self.C_li_tile = C_li_tile
  
  def set_C_li_double_tile(self, C_li_double_tile):
    self.C_li_double_tile = C_li_double_tile
  
  def set_C_li_triple_tile(self, C_li_triple_tile):
    self.C_li_triple_tile = C_li_triple_tile


  def propagate_values(self, group, computed_points, mpk, secret, title):
    """
    The function that will be called during the encrytpion process to propagate the values of the node

    Args:
      group (PairingGroup): The pairing group to be used
      computed_points (dict): The dictionary to store the computed points
      mpk (dict): The master public key
      secret (dict): The secret value for the current node
      title (str): The current propagate path
    """
    # Propagate the value to its child node, by default the atom node will always be the first node, hence
    # the corresponding polynomial will be the list that include the secret value.
    self.childNode.propagate_values(group, computed_points, mpk, [secret], title + "Atom" + str(self.id))


  def decrypt(self, key, group, title, decrypted_points):
    """The function that will be called during the decryption process to decrypt the node

    Args:
      key (dict): The private access key that will be used to decrypt the node
      group (PairingGroup): The pairing group to be used
      title (str): The current decryption path
      decrypted_points (dict): The dictionary to store the decrypted points

    Returns:
      result (tuple): A tuple that contains the status of the decryption and the value of the node
    """
    (status, value) = self.childNode.decrypt(key, group, title, decrypted_points)
    return (status, value)


  def serialize(self, group):
    """The function to serialize the atom node

    Args:
      group (PairingGroup): The pairing group to be used
    """

    # For each of the cryptographic values, we need to serialize them
    # Use the charm-crypto provided function "objectToBytes" to serialize the object
    self.C_li = objectToBytes(self.C_li, group)
    self.C_li_tile = objectToBytes(self.C_li_tile, group)
    self.C_li_double_tile = objectToBytes(self.C_li_double_tile, group)
    self.C_li_triple_tile = objectToBytes(self.C_li_triple_tile, group)
    self.index = objectToBytes(self.index, group)

    # Serialize the child node
    self.childNode.serialize(group)


  def deserialize(self, group):
    """The function to deserialize the atom node

    Args:
      group (PairingGroup): The pairing group to be used
    """

    # For each of the cryptographic values, we need to deserialize them
    # Use the charm-crypto provided function "bytesToObject" to deserialize the object
    self.C_li = bytesToObject(self.C_li, group)
    self.C_li_tile = bytesToObject(self.C_li_tile, group)
    self.C_li_double_tile = bytesToObject(self.C_li_double_tile, group)
    self.C_li_triple_tile = bytesToObject(self.C_li_triple_tile, group)
    self.index = bytesToObject(self.index, group)

    # Deserialize the child node
    self.childNode.deserialize(group)

  def __repr__(self):
    return str(self)
  
  def __str__(self):
    return self.id

  def getNodeType(self):
    return self.type