from charm.toolbox.pairinggroup import ZR

class tree_builder:

  def __init__(self, verbose=False):
    self.verbose = verbose

  # ====================================================================================================================================
  def build_tree_link(self, atom_nodes, attribute_nodes, link_nodes, attributes_set):
    '''
    Function to build the access tree.

    Args:
    - atom_nodes: list of atom nodes
    - attribute_nodes: list of attribute nodes
    - link_nodes: list of link nodes
    - attributes_set: set of attributes

    Returns:
    - self: the tree builder object
    '''
    self.atom_nodes = atom_nodes
    self.attribute_nodes = attribute_nodes
    self.link_nodes = link_nodes
    self.attributes_set = attributes_set
    return self


  def setup_atome_nodes_link(self, group, mpk, keys, random):
    """
    The function to setup encryption parameters the atom nodes and link nodes.

    Args:
        group (PairingGroup): the bilinear group used for the scheme
        mpk (dict): the master public key
        keys (dict): the symmetric keys for the data
        random (function): the random function provided by the caller, to generate random numbers
    """

    # Hash table to keep track of all the already computed points
    computed_points = {}
    for(index, key) in enumerate(keys):
      # Randomly select numbers from ZP
      si = random(ZR)
      noise_vector = random(ZR)

      target_sum = si + noise_vector
      target_index = index + 1

      self.atom_nodes[target_index].set_C_li(key * (mpk["e_gg_alpha"] ** target_sum))
      self.atom_nodes[target_index].set_C_li_tile(mpk["f1"] ** target_sum)
      self.atom_nodes[target_index].set_C_li_double_tile(mpk["f2"] ** target_sum)
      self.atom_nodes[target_index].set_C_li_triple_tile(mpk["f3"] ** noise_vector)
      
      # Propagate the values to the link nodes
      self.atom_nodes[target_index].propagate_values(group, computed_points, mpk, si, "")
