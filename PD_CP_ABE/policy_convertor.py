from charm.core.math.pairing import ZR
import re


from .Nodes.attribute_node import *
from .Nodes.atom_node import *
from .Nodes.link_node import *



class policy_convertor:
  """
  Class to analysis and parse policy string.
  ...

  Attributes
  ----------
  group : PairingGroup
    an instance of PairingGroup

  Methods
  -------
  generate_new_index(node_index_list)
    Generate a new index for a node.

  extract_logical_phases_list(policy)
    Extract the logical phases from a policy string.

  generate_atom_nodes(sizeof_atom_set, policy_str, node_index_list)
    Generate a list of atom nodes from a set of atoms.

  extract_attributes_list(policies_list)
    Get a set of attributes from a list of policies.

  generate_attribute_nodes(attribute_set, node_index_list)
    Generate a list of attribute nodes from a set of attributes.

  createAttribute_node(attrs, node_index_list)
    Create a list of attribute nodes.

  parse_boolean_expression(expression)
    Parse a boolean expression into its constituent parts.

  parse_policy(node, attribute_nodes, policy, link_nodes, node_index_list)
    Parse a policy.

  generate_link_nodes(atom_nodes, attribute_nodes, node_index_list)
    Generate a list of link nodes from a set of atom nodes.
  """

  # =========================================================================================
  def __init__(self, groupObj, verbose=True):
    self.group = groupObj



  # =========================================================================================
  def generate_new_index(self, node_index_list, node_index = -1):
    """Function to generate a new index for a node.

    Args:
      node_index_list (list): A list that contains all the pervious generated node indices

    Returns:
      node_index (ind): A new node index
    """

    # Generate a new index for the node
    # Check that the index is unique
    while (node_index in node_index_list):
      node_index = int(self.group.random(ZR))
    node_index_list.append(node_index)

    return node_index



  # =========================================================================================
  # Atom related functions
  def generate_atom_nodes(self, sizeof_atom_set, policy_str, node_index_list):
    """
    Generate a list of atom nodes from a set of atoms.

    Args:
    - sizeof_atom_set: the number of atoms
    - policy_str: a list of policies
    - node_index_list: a list of existing node indices

    Returns:
    - atom_nodes: a list of atom nodes
    """

    atom_nodes = {}

    for i in range(1, sizeof_atom_set + 1):
      node_index = self.generate_new_index(node_index_list)
      atom_nodes[i] = AtomNode(node_index, str(i), policy_str[i - 1])
    
    return atom_nodes




  # =========================================================================================
  # Attribute related functions
  def extract_attributes_list(self, policies_list):
    '''
    Get a set of attributes from a list of policies

    Args:
    - policies_list: a list of policies

    Returns:
    - target: a set of attributes
    '''
    target = set()

    # Regular expression to match the attributes, include letters, numbers and underscore
    pattern = r'\b(?!and\b|or\b)\w+\b'
    target = target | set(re.findall(pattern, " ".join(policies_list), flags=re.IGNORECASE))
    return target


  def generate_attribute_nodes(self, attribute_set, node_index_list):
    """
    Generate a list of attribute nodes from a set of attributes.

    Args:
    - attribute_set: a set of attributes
    - node_index_list: a list of existing node indices

    Returns:
    - attribute_nodes: a list of attribute nodes
    """

    attribute_nodes = {}

    for (index, attr) in enumerate(attribute_set):
      node_index = self.generate_new_index(node_index_list)
      attribute_nodes[attr] = AttributeNode(node_index, attr)

    return attribute_nodes


  def createAttribute_node(self, attrs, node_index_list):
    """
    Create a list of attribute nodes.

    Args:
    - attrs: a list of attributes
    - node_index_list: a list of existing node indices

    Returns:
    - attributes_set: a set of attributes
    - attribute_node: a list of attribute nodes
    """

    assert type(attrs) is list, "invalid type for policy_string_list"
    # Check every element in the list is a string
    for i in attrs:
      assert type(i) is str, "invalid type for element in policy_string_list"

    attributes_set = self.extract_attributes_list(attrs)
    attribute_node = self.generate_attribute_nodes(attributes_set, node_index_list)

    return attributes_set, attribute_node



  # =========================================================================================
  # Link related functions
  def parse_boolean_expression(self, expression):
    '''
    Function to parse a boolean expression into its constituent parts.

    Args:
    - expression: a string representing a boolean expression

    Returns:
    - a tuple of the form (left, operator, right) where:
        - left: the left operand
        - operator: the operator
        - right: the right operand
    '''
    # Remove leading and trailing whitespace
    expression = expression.strip()
        
    # If the expression is wrapped in outer parentheses, remove them
    if expression[0] == '(' and expression[-1] == ')':
      expression = expression[1:-1]   

    # Find the main operator (and/or) that splits the expression at the top level
    stack = []
    main_operator_pos = -1
    operator = None

    for i, char in enumerate(expression):
      if char == '(':
        stack.append(char)
      elif char == ')':
        stack.pop()
      elif not stack:  # We're at the top level
        if expression[i:i+4] == ' and':
          main_operator_pos = i + 1
          operator = 'and'
          break
        elif expression[i:i+3] == ' or':
          main_operator_pos = i + 1
          operator = 'or'
          break

    if main_operator_pos == -1:
      # No top-level and/or, so the expression is atomic
      return [expression]

    # Determine the operator and its length
    if operator == 'and':
      op_length = 3
    else:
      op_length = 2

    left = expression[:main_operator_pos].strip()
    right = expression[main_operator_pos+op_length:].strip()
    
    return left, operator, right
                


  def parse_policy(self, node, attribute_nodes, policy, link_nodes, node_index_list):
    # Parse the policy, get the left and right nodes and the operator
    left, operator, right = self.parse_boolean_expression(policy)

    evaluateLeft = None
    evaluateRight = None
    if not left.isalpha():
      # Check if this left policy corresponds to an existing node
      if (link_nodes.get(left) != None):
        node.setLeftNode(link_nodes[left])
        evaluateLeft = link_nodes[left]
      else:
        node_index = self.generate_new_index(node_index_list)
        childNode = LinkNode(left, node_index, None, None, None)
        link_nodes[left] = childNode
        evaluateLeft = self.parse_policy(childNode, attribute_nodes, left, link_nodes, node_index_list)
        node.setLeftNode(childNode)
    else:
        # Find the corresponding attribute node
        node.setLeftNode(attribute_nodes[left])
        evaluateLeft = attribute_nodes[left]

    
    if not right.isalpha():
      # Check if this right policy corresponds to an existing node
      if (link_nodes.get(right) != None):
        node.setRightNode(link_nodes[right])
        evaluateRight = link_nodes[right]
      else:
        node_index = self.generate_new_index(node_index_list)
        childNode = LinkNode(right, node_index, None, None, None)
        link_nodes[right] = childNode
        evaluateRight = self.parse_policy(childNode, attribute_nodes, right, link_nodes, node_index_list)
        node.setRightNode(childNode)
    else:
      # Find the corresponding attribute node
      node.setRightNode(attribute_nodes[right])
      evaluateRight = attribute_nodes[right]

    node.setThreshold(operator)
    if evaluateLeft == evaluateRight:
      node.setThreshold("or")
      return evaluateLeft
    return node



  def generate_link_nodes(self, atom_nodes, attribute_nodes, node_index_list):
    '''
    Function to generate a list of link nodes from a set of atom nodes.

    Args:
    - atom_nodes: a list of atom nodes
    - attribute_nodes: a list of attribute nodes
    - node_index_list: a list of existing node indices

    Returns:
    - link_nodes: a list of link nodes
    '''
    link_nodes = {}
    for atom in atom_nodes.values():
      if atom.policy.isalpha():
        # If it is just an attribute node, connect directly
        atom.set_chileNode(attribute_nodes[atom.policy])
        continue

      # Otherwise, generate a new link node and attach the index
      node_index = self.generate_new_index(node_index_list)
      childNode = LinkNode(atom.policy, node_index, None, None, None)
      link_nodes[childNode.id] = childNode

      # Keep parsing the policy
      self.parse_policy(childNode, attribute_nodes, atom.policy, link_nodes, node_index_list)
      atom.set_chileNode(childNode)
    return link_nodes

