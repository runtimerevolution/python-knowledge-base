# Pytest

> this document was inspired/copied from of
> [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html),
> [https://docs.pytest.org](https://docs.pytest.org) and
> [https://pytest-django.readthedocs.io/en/latest/](https://pytest-django.readthedocs.io/en/latest/)

Pytest is a Python testing framework that originated from the PyPy project. It can be used to write various types of
software tests, including unit tests, integration tests, end-to-end tests, and functional tests. Its features include
parametrized testing, fixtures, and assert re-writing.

> Python doesn't include Pytest out of the box, you must install it.
> Please check [https://docs.pytest.org](https://docs.pytest.org)

## Anatomy of a test

Pytest divides a test into four steps:

- **Arrange** is where we prepare everything for our test. This means pretty much everything except for the “act”.
This can mean preparing objects, starting/killing services, entering records into a database, or even things like
defining a URL to query, generating some credentials for a user that doesn't exist yet, or just waiting for some
process to finish.
- **Act** is the singular, state-changing action that kicks off the behavior we want to test. This typically takes the
form of a function/method call.
- **Assert** is where we take that measurement/observation on our test and apply our judgement to it.
- **Cleanup** is where the test picks up after itself, so other tests aren’t being accidentally influenced by it.

````python
import pytest

class TestStringMethods:  # A testcase
    
    # The individual tests are defined with methods whose names start with the 
    # letters test. This naming convention informs the test runner about which methods 
    # represent tests.
    def test_upper(self):  
        assert 'foo'.upper() == 'FOO'

    def test_isupper(self):
        assert 'FOO'.isupper() is True
        assert 'Foo'.isupper() is False

    def test_split(self):
        s = 'hello world'
        assert s.split() == ['hello', 'world']
        # check that s.split fails when the separator is not a string
        with pytest.raises(TypeError):
            s.split(2)
````

### Fixture

Fixtures are everything that needs to happen/exist in order to run a test.They're part of the **arrange** steps.

````python
import pytest


class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket
````

#### Fixture scopes

Fixtures are created when first requested by a test, and are destroyed based on their scope:

- **function**: the default scope, the fixture is destroyed at the end of the test.
- **class**: the fixture is destroyed during teardown of the last test in the class.
- **module**: the fixture is destroyed during teardown of the last test in the module.
- **package**: the fixture is destroyed during teardown of the last test in the package.
- **session**: the fixture is destroyed at the end of the test session.

```python
@pytest.fixture(scope="session")
def smtp_connection():
    # the returned fixture value will be shared for
    # all tests requesting it
    ...
```

### Command Line

The pytest module can be used from the command line to run tests from modules, classes or even individual test
methods:

```bash
pytest test_module1 test_module2
pytest test_module.TestClass
pytest test_module.TestClass.test_method
```

For a list of all the command-line options:

```bash
pytest -h
```

## Assertions

Pytest allows you to use the standard Python **assert** for verifying expectations and values in Python tests.

### Custom error message

Assert supports a message, which should be used to make assert statements more clear.

````python
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
````

## Parametrize

The builtin _pytest.mark.parametrize_ decorator enables parametrization of arguments for a test function.

```python
import pytest

@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

which can also be declared as

```python
@pytest.mark.parametrize("test_input", ["3+5", "2+4", "6*9"])
@pytest.mark.parametrize("expected", [8, 6, 42])
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

## Anatomy of a Django test

> To use Pytest with Django you must install [https://pytest-django.readthedocs.io](https://pytest-django.readthedocs.io)

```python
import pytest

from myapp.models import Animal


@pytest.fixture(scope="function")
def cat():
    Animal.objects.create(name="cat", sound="meow")


@pytest.fixture(scope="function")
def lion():
    Animal.objects.create(name="lion", sound="roar")


@pytest.fixture(scope="function")
def felines(lion, cat):
    ...

@pytest.mark.django_db
def test_animals_can_speak(felines):
    """Animals that can speak are correctly identified"""
    lion = Animal.objects.get(name="lion")
    cat = Animal.objects.get(name="cat")

    assert lion.speak() == 'The lion says "roar"'
    assert cat.speak() == 'The cat says "meow"'
```

### Why would I use this instead of Django’s manage.py test command?

Running the test suite with pytest offers some features that are not present in Django’s standard test mechanism:

- Less boilerplate: no need to import unittest, create a subclass with methods. Just write tests as regular functions.
- Manage test dependencies with fixtures.
- Run tests in multiple processes for increased speed.
- There are a lot of other nice plugins available for pytest.
- Easy switching: Existing unittest-style tests will still work without any modifications.
