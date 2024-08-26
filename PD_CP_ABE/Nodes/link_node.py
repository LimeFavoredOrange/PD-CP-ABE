from charm.core.math.pairing import ZR
from charm.core.engine.util import objectToBytes, bytesToObject
from ..lagrange import lagrange_polynomial, lagrange_polynomial_bilinear_mapping
from ..polynomial_generator import generatePolynomial, calculatePolynomial


class LinkNode:
  """
  A class used to represent an Link node

  Attributes
  ----------
  id : str
    a unique identifier for the node
  type : str
    the type of the node
  threshold : int
    the threshold of the node
  index : int
    the index of the node
  leftNode : Node
    the left node of the node
  rightNode : Node
    the right node of the node
  shareValue : tuple
    the share value of the node
  path : str
    the path of the node

  Methods
  -------
  setThreshold(threshold)
    Set the threshold of the node
  setLeftNode(leftNode)
    Set the left node of the node
  setRightNode(rightNode)
    Set the right node of the node
  getTitle()
    Get the title of the node
  getNodeType()
    Get the type of the node
  addToDecryptedPoints(title, decrypted_points, value)
    Add the node to the decrypted points
  propagate_values(group, computed_points, mpk, polynomial, title)
    Propagate the values of the node
  decrypt(key, group, title, decrypted_points)
    Decrypt the node
  serialize(group)
    Serialize the node
  deserialize(group)
    Deserialize the node
  """

  # The init function of the LinkNode class
  def __init__(self, id, index, threshold, leftNode, rightNode):
    self.id = id
    self.type = "LINK"
    
    # The threshold type for the node (And/Or)
    self.threshold = 2 if threshold == "and" else 1
    self.index = index

    self.leftNode = leftNode
    self.rightNode = rightNode

    # Initially, the node will not have a share value
    self.shareValue = (False, 0)
    self.path = ""

  def setThreshold(self, threshold):
    self.threshold = 2 if threshold == "and" else 1

  def setLeftNode(self, leftNode):
    self.leftNode = leftNode

  def setRightNode(self, rightNode):
    self.rightNode = rightNode

  def getNodeType(self):
    return self.type


  def addToDecryptedPoints(self, title, decrypted_points, value):
    """Function to add the node to the decrypted points

    Args:
      title (str): The current decryption path
      decrypted_points (dict): The dictionary of decrypted points
      value (tuple): The tuple of the decrypted value
    """
    if title == self.path:
      # Only keep track of the value if it is part of the current path
      # Because only the nodes in the current path will be shared between 
      # the nodes
      decrypted_points[self] = value


  def compute_share(self, group, points):
    polynomial = lagrange_polynomial_bilinear_mapping(group, points)
    return polynomial(0)

  def propagate_values(self, group, computed_points, mpk, polynomial, title):
    """
    The function that will be called during the encryption process to propagate the values of the node

    Args:
        group (PairingGroup): The pairing group to be used
        computed_points (dict): The dictionary to store the computed points
        mpk (dict): THe master public key
        polynomial (list/function): The polynomial to be used to calculate the secret value
        title (str): The current propagate path
    """

    # The value of the polynomial at x = index is the secret value
    secret = calculatePolynomial(polynomial, self.index, group) if isinstance(polynomial, list) else polynomial(self.index)

    # Add the current node to the the computed points
    if self not in computed_points:
      # First time to propagate to this node
      # Add it to the computed points
      computed_points[self] = (self.index, secret)

      # Set the path of the node (by default)
      self.path = title

    # Generate the polynomial for this secret value
    polynomial = generatePolynomial(self.threshold, secret, group)

    # If both children of the current node have values or do not have values, then continue to propagate and calculate
    # Also it the threshold is 1, then the node is an OR node, so we need to propagate to both children as well.
    if (self.leftNode not in computed_points and self.rightNode not in computed_points) or (self.leftNode in computed_points and self.rightNode in computed_points) or (self.threshold == 1):
      self.leftNode.propagate_values(group, computed_points, mpk, polynomial, title + "->" + str(self))
      self.rightNode.propagate_values(group, computed_points, mpk, polynomial, title + "->" + str(self))
    elif self.leftNode not in computed_points:
      # If the left node does not have a value, then use the right node and the current node to generate a new polynomial
      polynomial = lagrange_polynomial(group, [computed_points[self.rightNode], (group.init(ZR, 0), secret)])
      self.shareValue = (True, 2)
      # Propagate the value to the left node
      self.leftNode.propagate_values(group, computed_points, mpk, polynomial, title + "->" + str(self))
    elif self.rightNode not in computed_points:
      # If the right node does not have a value, then use the left node and the current node to generate a new polynomial
      polynomial = lagrange_polynomial(group, [computed_points[self.leftNode], (group.init(ZR, 0), secret)])
      self.shareValue = (True, 1)
      # Propagate the value to the right node
      self.rightNode.propagate_values(group, computed_points, mpk, polynomial, title + "->" + str(self))



  def decrypt(self, key, group, path, decrypted_points):
    """
    Function to decrypt the node

    Args:
      key (dict): The private key to be used for decryption
      group (PairingGroup): The pairing group to be used
      title (str): The current decryption path
      decrypted_points (dict): The dictionary of decrypted points

    Returns:
        _type_: _description_
    """

    title = path + f"->{self}"


    # Check the share value of the node
    shareValue, shareSide = self.shareValue
    shareTarget = self.leftNode if shareSide == 1 else self.rightNode

    leftValue = None
    rightValue = None
    
    if self.threshold == 2:
      # If this is an and node, then both nodes must be decrypted
      if shareValue and shareSide == 1:
        if shareTarget in decrypted_points:
          leftValue = decrypted_points[shareTarget]
        else:
          (status, leftValue) = shareTarget.decrypt(key, group, shareTarget.path, decrypted_points)
          if status == False:
            return False, 0
      else:
        (status, leftValue) = self.leftNode.decrypt(key, group, title, decrypted_points)
        if status == False:
          return False, 0
      
      if shareValue and shareSide == 2:
        if shareTarget in decrypted_points:
          rightValue = decrypted_points[shareTarget]
        else:
          (status, rightValue) = shareTarget.decrypt(key, group, shareTarget.path, decrypted_points)
          if status == False:
            return False, 0
      else:
        (status, rightValue) = self.rightNode.decrypt(key, group, title, decrypted_points)
        if status == False:
          return False, 0

      value = self.compute_share(group, [(self.leftNode.index, leftValue), (self.rightNode.index, rightValue)])
      self.addToDecryptedPoints(path, decrypted_points, value)
      return True, value
    else:
      (status, leftValue) = self.leftNode.decrypt(key, group, title, decrypted_points)
      if status == True:
        value = self.compute_share(group, [(self.leftNode.index, leftValue)])
        self.addToDecryptedPoints(path, decrypted_points, value)
        return True, value
      
      (status, rightValue) = self.rightNode.decrypt(key, group, title, decrypted_points)
      if status == True:
        value = self.compute_share(group, [(self.rightNode.index, rightValue)])
        self.addToDecryptedPoints(path, decrypted_points, value)
        return True, value

    return False, 0



  def serialize(self, group):
    """
    Function to serialize the node

    Args:
        group (PairingGroup): The pairing group to be used
    """
    self.index = objectToBytes(self.index, group)
    self.leftNode.serialize(group)
    self.rightNode.serialize(group)


  def deserialize(self, group):
    """
    Function to deserialize the node

    Args:
        group (PairingGroup): The pairing group to be used
    """
    self.index = bytesToObject(self.index, group)
    self.leftNode.deserialize(group)
    self.rightNode.deserialize(group)

  def __repr__(self):
    return str(self)

  def __str__(self):
    return self.id