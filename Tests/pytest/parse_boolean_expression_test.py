import pytest
import os
import sys
from charm.toolbox.pairinggroup import PairingGroup



project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path: sys.path.append(project_root)

from PD_CP_ABE import policy_convertor

def get_instance():
    return policy_convertor.policy_convertor(PairingGroup('SS512'))

def test_no_operators():
    target = get_instance()
    assert target.parse_boolean_expression("x") == ["x"]

def test_with_and_operator():
    target = get_instance()
    assert target.parse_boolean_expression("x and y") == ('x', 'and', 'y')

def test_with_or_operator():
    target = get_instance()
    assert target.parse_boolean_expression("x or y") == ('x', 'or', 'y')

def test_nested_parentheses():
    target = get_instance()
    assert target.parse_boolean_expression("((x))") == ["(x)"]

def test_operators_inside_parentheses():
    target = get_instance()
    assert target.parse_boolean_expression("(x and y) or z") == ('(x and y)', 'or', 'z'), "Test with operators inside parentheses failed"




