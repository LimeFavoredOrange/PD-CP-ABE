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


# Test for 2 atoms -> and case, no share attribute 
def test_decrypt_two_nodes_and_no_share(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A and B)", "(C and D)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Hello']}, '2': {'policy': '(C and D)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Hello']}, '2': {'policy': '(C and D)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["C", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(C and D)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["A", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(C and D)', 'Decryptable': False }}

    key = target.keygen(mpk, msk, ["B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(C and D)', 'Decryptable': False }}



# Test for multiple atoms -> and case, no share attribute
def test_decrypt_multiple_nodes_and_no_share(abe_instance):
    target, mpk, msk = abe_instance
    # Test for 8 messages for this case
    messages = ["Text1", "Text2", "Text3", "Text4", "Text5", "Text6", "Text7", "Text8"]
    access_policies = ["(A and B)", "(C and D)", "(E and F)", "(G and H)", "(I and J)", "(K and L)", "(M and N)", "(O and P)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Text1']}, '2': {'policy': '(C and D)', 'Decryptable': ['Text2']}, '3': {'policy': '(E and F)', 'Decryptable': ['Text3']}, '4': {'policy': '(G and H)', 'Decryptable': ['Text4']}, '5': {'policy': '(I and J)', 'Decryptable': ['Text5']}, '6': {'policy': '(K and L)', 'Decryptable': ['Text6']}, '7': {'policy': '(M and N)', 'Decryptable': ['Text7']}, '8': {'policy': '(O and P)', 'Decryptable': ['Text8']}}

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E", "F", "G", "H"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Text1']}, '2': {'policy': '(C and D)', 'Decryptable': ['Text2']}, '3': {'policy': '(E and F)', 'Decryptable': ['Text3']}, '4': {'policy': '(G and H)', 'Decryptable': ['Text4']}, '5': {'policy': '(I and J)', 'Decryptable': False}, '6': {'policy': '(K and L)', 'Decryptable': False}, '7': {'policy': '(M and N)', 'Decryptable': False}, '8': {'policy': '(O and P)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["I", "J", "K", "L", "M", "N", "O", "P"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(C and D)', 'Decryptable': False}, '3': {'policy': '(E and F)', 'Decryptable': False}, '4': {'policy': '(G and H)', 'Decryptable': False}, '5': {'policy': '(I and J)', 'Decryptable': ['Text5']}, '6': {'policy': '(K and L)', 'Decryptable': ['Text6']}, '7': {'policy': '(M and N)', 'Decryptable': ['Text7']}, '8': {'policy': '(O and P)', 'Decryptable': ['Text8']}}

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "I", "J", "K", "L"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Text1']}, '2': {'policy': '(C and D)', 'Decryptable': ['Text2']}, '3': {'policy': '(E and F)', 'Decryptable': False}, '4': {'policy': '(G and H)', 'Decryptable': False}, '5': {'policy': '(I and J)', 'Decryptable': ['Text5']}, '6': {'policy': '(K and L)', 'Decryptable': ['Text6']}, '7': {'policy': '(M and N)', 'Decryptable': False}, '8': {'policy': '(O and P)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["E", "F", "G", "H", "M", "N", "O", "P"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(C and D)', 'Decryptable': False}, '3': {'policy': '(E and F)', 'Decryptable': ['Text3']}, '4': {'policy': '(G and H)', 'Decryptable': ['Text4']}, '5': {'policy': '(I and J)', 'Decryptable': False}, '6': {'policy': '(K and L)', 'Decryptable': False}, '7': {'policy': '(M and N)', 'Decryptable': ['Text7']}, '8': {'policy': '(O and P)', 'Decryptable': ['Text8']}}


# Test for 2atoms -> or case, no share attribute
def test_decrypt_two_nodes_or_no_share(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A or B)", "(C and D)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(C and D)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(C and D)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(C and D)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["C", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}, '2': {'policy': '(C and D)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["A", "D"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(C and D)', 'Decryptable': False }}

    key = target.keygen(mpk, msk, ["B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(C and D)', 'Decryptable': False }}


# Test for multiple atoms -> or case, no share attribute
def test_decrypt_multiple_nodes_or_no_share(abe_instance):
    target, mpk, msk = abe_instance
    # Test for 8 messages for this case
    messages = ["Text1", "Text2", "Text3", "Text4", "Text5", "Text6", "Text7", "Text8"]
    access_policies = ["(A or B)", "(C or D)", "(E or F)", "(G or H)", "(I or J)", "(K or L)", "(M or N)", "(O or P)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "C", "D", "F", "G", "H", "J", "L", "M", "N", "P"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Text1']}, '2': {'policy': '(C or D)', 'Decryptable': ['Text2']}, '3': {'policy': '(E or F)', 'Decryptable': ['Text3']}, '4': {'policy': '(G or H)', 'Decryptable': ['Text4']}, '5': {'policy': '(I or J)', 'Decryptable': ['Text5']}, '6': {'policy': '(K or L)', 'Decryptable': ['Text6']}, '7': {'policy': '(M or N)', 'Decryptable': ['Text7']}, '8': {'policy': '(O or P)', 'Decryptable': ['Text8']}}

    key = target.keygen(mpk, msk, ["G", "L", "M", "P"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}, '2': {'policy': '(C or D)', 'Decryptable': False}, '3': {'policy': '(E or F)', 'Decryptable': False}, '4': {'policy': '(G or H)', 'Decryptable': ['Text4']}, '5': {'policy': '(I or J)', 'Decryptable': False}, '6': {'policy': '(K or L)', 'Decryptable': ['Text6']}, '7': {'policy': '(M or N)', 'Decryptable': ['Text7']}, '8': {'policy': '(O or P)', 'Decryptable': ['Text8']}}


# Test for 2 atoms -> and case, share attribute
def test_decrypt_two_nodes_and_share(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A and B)", "(A and C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Hello']}, '2': {'policy': '(A and C)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Hello']}, '2': {'policy': '(A and C)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(A and C)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(A and C)', 'Decryptable': False}}

# Test for multiple atoms -> and case, share attribute
def test_decrypt_multiple_nodes_and_share(abe_instance):
    target, mpk, msk = abe_instance
    # Test for 8 messages for this case
    messages = ["Text1", "Text2", "Text3", "Text4", "Text5", "Text6", "Text7", "Text8"]
    access_policies = ["(A and B)", "(A and C)", "(A and D)", "(A and E)", "(A and F)", "(A and G)", "(A and H)", "(A and I)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E", "F", "G", "H", "I"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Text1']}, '2': {'policy': '(A and C)', 'Decryptable': ['Text2']}, '3': {'policy': '(A and D)', 'Decryptable': ['Text3']}, '4': {'policy': '(A and E)', 'Decryptable': ['Text4']}, '5': {'policy': '(A and F)', 'Decryptable': ['Text5']}, '6': {'policy': '(A and G)', 'Decryptable': ['Text6']}, '7': {'policy': '(A and H)', 'Decryptable': ['Text7']}, '8': {'policy': '(A and I)', 'Decryptable': ['Text8']}}

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E", "F", "G", "H"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': ['Text1']}, '2': {'policy': '(A and C)', 'Decryptable': ['Text2']}, '3': {'policy': '(A and D)', 'Decryptable': ['Text3']}, '4': {'policy': '(A and E)', 'Decryptable': ['Text4']}, '5': {'policy': '(A and F)', 'Decryptable': ['Text5']}, '6': {'policy': '(A and G)', 'Decryptable': ['Text6']}, '7': {'policy': '(A and H)', 'Decryptable': ['Text7']}, '8': {'policy': '(A and I)', 'Decryptable': False}}


    key = target.keygen(mpk, msk, ["A", "D", "F", "H"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(A and C)', 'Decryptable': False}, '3': {'policy': '(A and D)', 'Decryptable': ['Text3']}, '4': {'policy': '(A and E)', 'Decryptable': False}, '5': {'policy': '(A and F)', 'Decryptable': ['Text5']}, '6': {'policy': '(A and G)', 'Decryptable': False}, '7': {'policy': '(A and H)', 'Decryptable': ['Text7']}, '8': {'policy': '(A and I)', 'Decryptable': False}}


    access_policies = ["(A and B)", "(A and C)", "(B and D)", "(C and E)", "(E and A)", "(B and C)", "(B and H)", "(A and B)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)
    
    key = target.keygen(mpk, msk, ["A", "C", "E", "H"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A and B)', 'Decryptable': False}, '2': {'policy': '(A and C)', 'Decryptable': ['Text2']}, '3': {'policy': '(B and D)', 'Decryptable': False}, '4': {'policy': '(C and E)', 'Decryptable': ['Text4']}, '5': {'policy': '(E and A)', 'Decryptable': ['Text5']}, '6': {'policy': '(B and C)', 'Decryptable': False}, '7': {'policy': '(B and H)', 'Decryptable': False}}


# Test for 2 atoms -> or case, share attribute
def test_decrypt_two_nodes_or_share(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["(A or B)", "(A or C)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(A or C)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(A or C)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': False}, '2': {'policy': '(A or C)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Hello']}, '2': {'policy': '(A or C)', 'Decryptable': ['World']}}


# Test for multiple atoms -> or case, share attribute
def test_decrypt_multiple_nodes_or_share(abe_instance):
    target, mpk, msk = abe_instance
    # Test for 8 messages for this case
    messages = ["Text1", "Text2", "Text3", "Text4", "Text5", "Text6", "Text7", "Text8"]
    access_policies = ["(A or B)", "(A or C)", "(B or D)", "(C or E)", "(E or A)", "(B or C)", "(B or H)", "(A or H)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E", "F", "G", "H"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Text1']}, '2': {'policy': '(A or C)', 'Decryptable': ['Text2']}, '3': {'policy': '(B or D)', 'Decryptable': ['Text3']}, '4': {'policy': '(C or E)', 'Decryptable': ['Text4']}, '5': {'policy': '(E or A)', 'Decryptable': ['Text5']}, '6': {'policy': '(B or C)', 'Decryptable': ['Text6']}, '7': {'policy': '(B or H)', 'Decryptable': ['Text7']}, '8': {'policy': '(A or H)', 'Decryptable': ['Text8']}}

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E", "F", "G", "H", "I"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Text1']}, '2': {'policy': '(A or C)', 'Decryptable': ['Text2']}, '3': {'policy': '(B or D)', 'Decryptable': ['Text3']}, '4': {'policy': '(C or E)', 'Decryptable': ['Text4']}, '5': {'policy': '(E or A)', 'Decryptable': ['Text5']}, '6': {'policy': '(B or C)', 'Decryptable': ['Text6']}, '7': {'policy': '(B or H)', 'Decryptable': ['Text7']}, '8': {'policy': '(A or H)', 'Decryptable': ['Text8']}}

    key = target.keygen(mpk, msk, ["A", "D", "F", "H"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '(A or B)', 'Decryptable': ['Text1']}, '2': {'policy': '(A or C)', 'Decryptable': ['Text2']}, '3': {'policy': '(B or D)', 'Decryptable': ['Text3']}, '4': {'policy': '(C or E)', 'Decryptable': False}, '5': {'policy': '(E or A)', 'Decryptable': ['Text5']}, '6': {'policy': '(B or C)', 'Decryptable': False}, '7': {'policy': '(B or H)', 'Decryptable': ['Text7']}, '8': {'policy': '(A or H)', 'Decryptable': ['Text8']}}


def test_decrypt_multiple_atom_with_connection_and_success(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["((A and B) and C)", "((D and E) and F)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E", "F"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': ['Hello']}, '2': {'policy': '((D and E) and F)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': ['Hello']}, '2': {'policy': '((D and E) and F)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A", "B", "D", "E", "F"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}, '2': {'policy': '((D and E) and F)', 'Decryptable': ['World']}}


def test_decrypt_multiple_atom_with_connection_and_fail(abe_instance):
    target, mpk, msk = abe_instance
    messages = ["Hello", "World"]
    access_policies = ["((A and B) and C)", "((D and E) and F)"]
    ciphers, access_tree = target.encrypt(mpk, messages, access_policies)

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "E"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': ['Hello']}, '2': {'policy': '((D and E) and F)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A", "B", "C", "D", "F"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': ['Hello']}, '2': {'policy': '((D and E) and F)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A", "B", "C", "E", "F"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': ['Hello']}, '2': {'policy': '((D and E) and F)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A", "B", "C", "F"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': ['Hello']}, '2': {'policy': '((D and E) and F)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A", "B", "C"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': ['Hello']}, '2': {'policy': '((D and E) and F)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["A", "B"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}, '2': {'policy': '((D and E) and F)', 'Decryptable': False}}

    key = target.keygen(mpk, msk, ["D", "E", "F"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}, '2': {'policy': '((D and E) and F)', 'Decryptable': ['World']}}

    key = target.keygen(mpk, msk, ["D", "E"], "Alice")
    decrypted_messages = target.decrypt(access_tree, key, ciphers)
    assert decrypted_messages == {'1': {'policy': '((A and B) and C)', 'Decryptable': False}, '2': {'policy': '((D and E) and F)', 'Decryptable': False}}
