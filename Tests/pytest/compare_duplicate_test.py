from script_test_myabe import test as test_myabe
from script_test_bsw07 import test as test_bsw07


def test_compare_duplicate():
    print("Running test_compare_duplicate")
    myABE_result, myABE_total, myABE_decryptable = test_myabe(duplicate=True)
    bsw07_result, bsw07_total, bsw07_decryptable = test_bsw07(duplicate=True)
    assert myABE_total == bsw07_total
    assert myABE_decryptable == bsw07_decryptable
    for key, value in myABE_result.items():
        assert value == bsw07_result[key]

if __name__ == "__main__":
    test_compare_duplicate()


