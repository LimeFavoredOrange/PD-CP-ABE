# from abe import h1_hash_from_binary_to_G0
from charm.core.engine.util import objectToBytes, bytesToObject
from charm.toolbox.pairinggroup import pair
from ..polynomial_generator import calculatePolynomial



class AttributeNode:
  """
  A class used to represent an Attribute node

  Attributes
  ----------
  type : str
    the type of the node
  index : int
    the index of the node
  cipher : dict
    a dictionary that contains the ciphers of the node
  path : str
    the path of the node
  attribute : str
    the attribute of the node
  """

  # The init function of the AttributeNode class
  def __init__(self, index, value):		
    self.type = "ATTR"
    self.index = index

    self.cipher = {}
    self.path = ""
    
    # Assume that the value of an attribute node is in uppercase.
    self.attribute = value.upper() 


  def addCipher(self, title, cipher_down, cipher_up):
    """
    Function to add a cipher to the node

    Args:
        title (str): The current path of the node
        cipher_down (PairingElement): A cryptographic element
        cipher_up (PairingElement): A cryptographic element
    """
    self.cipher[title] = [cipher_down, cipher_up]
  

  def propagate_values(self, group, computed_points, mpk, polynomial, title):
    """
    Function to propagate the values

    Args:
        group (PairingGroup): The pairing group to be used
        computed_points (dict): The dictionary that contains the computed points
        mpk (dict): The master public key
        polynomial (list/function): The polynomial to be used
        title (str): The current path of the node
    """
    # If the given polynomial is a list, then we can use it to calculate the secret value.
    # If the given polynomial is a function, then we can use it to calculate the secret value.
    # The value of the polynomial at x = index is the secret value
    secret = calculatePolynomial(polynomial, self.index, group) if isinstance(polynomial, list) else polynomial(self.index)

    # If this is the first time to reach this node, then we will store the computed point in the computed_points dictionary
    if self.path == "": 
      computed_points[self] = (self.index, secret)
      self.path = title

    # Calculate the ciphers
    cipher_down = mpk['g'] ** secret
    cipher_up = mpk['h1'](self.attribute.encode('utf-8')) ** secret

    # Add the ciphers to the node
    if title not in self.cipher:
      self.addCipher(title, cipher_down, cipher_up)



  def decrypt(self, key, group, title, decrypted_points):
    """
    Function to decrypt the node

    Args:
        key (dict): The private access key of the user
        group (PairingGroup): The pairing group to be used
        title (str): The current decryption path
        decrypted_points (dict): The dictionary that contains the decrypted points

    Returns:
        result (tuple): A tuple that contains the result of the decryption
    """

    # If the attribute is not in the key, then return
    if (self.attribute not in key["attributes_set"]):
      return False, 0
    
    # Get the key information
    key_info = (key['attributes_keys'][self.attribute+"_down"], key['attributes_keys'][self.attribute+"_up"])
    point = self.cipher[self.path] if title not in self.cipher else self.cipher[title]

    # Decrypt the node
    value = (pair(key_info[0], point[0])) / pair(key_info[1], point[1])

    # if title.startswith(self.path):
    if title == self.path:
      decrypted_points[self] = value
    
    return True, value


  def serialize(self, group):
    """
    Function to serialize the node

    Args:
      group (PairingGroup): The pairing group to be used
    """
    self.index = objectToBytes(self.index, group)
    # self.polyValue = (objectToBytes(self.polyValue[0], group), objectToBytes(self.polyValue[1], group))

    # Loop through the ciphers and serialize them
    for key in self.cipher.keys():
      self.cipher[key][0] = objectToBytes(self.cipher[key][0], group)
      self.cipher[key][1] = objectToBytes(self.cipher[key][1], group)

  def deserialize(self, group):
    """
    Function to deserialize the node

    Args:
      group (PairingGroup): The pairing group to be used
    """
    self.index = bytesToObject(self.index, group)
    # self.polyValue =  (bytesToObject(self.polyValue[0], group), bytesToObject(self.polyValue[1], group))

    # Loop through the ciphers and serialize them
    for key in self.cipher.keys():
      self.cipher[key][0] = bytesToObject(self.cipher[key][0], group)
      self.cipher[key][1] = bytesToObject(self.cipher[key][1], group)


  def __repr__(self):
    return str(self)

  def __str__(self):
    return self.attribute

  def getNodeType(self):
    return self.type