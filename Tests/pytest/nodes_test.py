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

# Atom node testing
def test_atom_nodes(abe_instance):
    target, mpk, _ = abe_instance
    messages = ["Hello", "World", "HEllo"]
    access_policies = ["(A and B)", "(A or B)", "(A or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    atom = access_tree.atom_nodes[1]
    assert str(atom) == "1"
    assert atom.getNodeType() == "Atom"
    assert repr(atom) == "1"

def test_attribute_nodes(abe_instance):
    target, mpk, _ = abe_instance
    messages = ["Hello", "World", "HEllo"]
    access_policies = ["(A and B)", "(A or B)", "(A or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    attribute = access_tree.attribute_nodes["A"]
    assert str(attribute) == "A"
    assert repr(attribute) == "A"
    assert attribute.getNodeType() == "ATTR"

def test_link_nodes(abe_instance):
    target, mpk, _ = abe_instance
    messages = ["Hello", "World", "HEllo"]
    access_policies = ["(A and B)", "(A or B)", "(A or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    print(access_tree.link_nodes)
    link = access_tree.link_nodes['(A and B)']
    assert str(link) == "(A and B)"
    assert repr(link) == "(A and B)"
    assert link.getNodeType() == "LINK"
