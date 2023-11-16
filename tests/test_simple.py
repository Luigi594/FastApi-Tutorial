# always call your test files like test_*.py
# run the test with the command: pytest


def test_add_two():
    x = 1
    y = 2

    assert x + y == 3


def test_dict_contains():
    d = {"a": 1, "b": 2}
    expected = {"a": 1}

    # check if expected is a subset of d
    assert (
        expected.items() <= d.items()
    ), "The actual output is missing some key-value pairs"
