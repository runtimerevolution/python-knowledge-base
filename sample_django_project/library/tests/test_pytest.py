import pytest


class TestStringMethods:
    def test_upper(self):
        assert 'foo'.upper() == 'FOO', "Test string uppercase equal"

    def test_isupper(self):
        assert 'FOO'.isupper() is True, "Test string uppercase True"
        assert 'Foo'.isupper() is False, "Test string uppercase False"

    def test_split(self):
        s = 'hello world'
        assert s.split() == ['hello', 'world'], "Test split string"

        with pytest.raises(TypeError, match="must be str or None, not int"):
            s.split(2)
