# Unittest

> this document was inspired/copied from of [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html) and 
> [https://docs.djangoproject.com/en/4.1/topics/testing/overview/](https://docs.djangoproject.com/en/4.1/topics/testing/overview/)


The unittest unit testing framework was originally inspired by JUnit and has a similar flavor as major unit testing 
frameworks in other languages. It supports test automation, sharing of setup and shutdown code for tests, aggregation 
of tests into collections, and independence of the tests from the reporting framework.

Unittest supports some important concepts in an object-oriented way:

- test fixture: A test fixture represents the preparation needed to perform one or more tests, and any associated cleanup actions. This may involve, for example, creating temporary or proxy databases, directories, or starting a server process.
- test case: A test case is the individual unit of testing. It checks for a specific response to a particular set of inputs. unittest provides a base class, TestCase, which may be used to create new test cases.
- test suite: A test suite is a collection of test cases, test suites, or both. It is used to aggregate tests that should be executed together.
- test runner: A test runner is a component which orchestrates the execution of tests and provides the outcome to the user. The runner may use a graphical interface, a textual interface, or return a special value to indicate the results of executing the tests.

## Anatomy of a test

````python
import unittest

class TestStringMethods(unittest.TestCase):  # A testcase is created by 
                                             # subclassing unittest.TestCase
    
    # The individual tests are defined with methods whose names start with the 
    # letters test. This naming convention informs the test runner about which methods 
    # represent tests.
    def test_upper(self):  
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    # provides a command-line interface to the test script
    unittest.main()
````

### Fixture

A working environment that has a **setUp()** and **tearDown()** the testing code is called a **test fixture**. 

A new TestCase instance is created as a unique test fixture used to execute each individual test method. Thus 
**setUp()**, **tearDown()**, and **__init__()** will be called once per test.

````python
import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()
````

If the **setUp()** method raises an exception while the test is running, the framework will consider the test to have
suffered an error, and the test method will not be executed. If **setUp()** succeeded, **tearDown()** will be run 
whether the test method succeeded or not.

By default, **setUp()** and **tearDown()** do nothing.

### Command Line

The unittest module can be used from the command line to run tests from modules, classes or even individual test
methods:

```bash
python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method
```

You can pass in a list with any combination of module names, and fully qualified class or method names.

Test modules can be specified by file path as well:

```bash
python -m unittest tests/test_something.py
```

This allows you to use the shell filename completion to specify the test module. The file specified must still be importable as a module. The path is converted to a module name by removing the ‘.py’ and converting path separators into ‘.’. If you want to execute a test file that isn’t importable as a module you should execute the file directly instead.

You can run tests with more detail (higher verbosity) by passing in the -v flag:

```bash
python -m unittest -v test_module
```

When executed without arguments Test Discovery is started:

```bash
python -m unittest
```

For a list of all the command-line options:

```bash
python -m unittest -h
```

## Assertions

The TestCase class provides several assert methods to check for and report failures.

| Method                                        | Checks that                                                    | 
|-----------------------------------------------|----------------------------------------------------------------|
| assertEqual(a, b)                             | a == b                                                         | 
| assertNotEqual(a, b)                          | a != b                                                         | 
| assertTrue(x)                                 | bool(x) is True                                                |
| assertFalse(x)                                | bool(x) is False                                               |
| assertIs(a, b)                                | a is b                                                         |
| assertIsNot(a, b)                             | a is not b                                                     |
| assertIsNone(x)                               | x is None                                                      |
| assertIsNotNone(x)                            | x is not None                                                  |
| assertIn(a, b)                                | a in b                                                         |
| assertNotIn(a, b)                             | a not in b                                                     |
| assertIsInstance(a, b)                        | isinstance(a, b)                                               |
| assertNotIsInstance(a, b)                     | not isinstance(a, b)                                           |
| assertRaises(exc, fun, *args, **kwds)         | fun(*args, **kwds) raises exc                                  |
| assertRaisesRegex(exc, r, fun, *args, **kwds) | fun(*args, **kwds) raises exc and the message matches regex r  |
| assertWarns(warn, fun, *args, **kwds)         | fun(*args, **kwds) raises warn                                 |
| assertWarnsRegex(warn, r, fun, *args, **kwds) | fun(*args, **kwds) raises warn and the message matches regex r |
| assertLogs(logger, level)                     | The with block logs on logger with minimum level               |
| assertNoLogs(logger, level)                   | The with block does not log on logger with minimum level       |
	
### Custom error message

All the assert methods accept a **msg** argument that, if specified, is used as the error message on failure.

Note that the msg keyword argument can be passed to **assertRaises()**, **assertRaisesRegex()**, **assertWarns()**,
**assertWarnsRegex()** only when they are used as a __context manager__.

````python
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):  
        self.assertEqual('foo'.upper(), 'FOO', "Test string uppercase equal")

    def test_isupper(self):
        self.assertTrue('FOO'.isupper(), "Test string uppercase True")
        self.assertFalse('Foo'.isupper(), "Test string uppercase False")

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

        with self.assertRaises(TypeError, "check that s.split fails when the separator is not a string"):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
````

## Anatomy of a Django test

```python
from django.test import TestCase  # is a subclass of unittest.TestCase that 
                                  # runs each test inside a transaction to provide isolation
from myapp.models import Animal

class AnimalTestCase(TestCase):
    # Django provides an additional way of defining fixtures
    # these can be generated by running:
    #    python manage.py dumpdata animal_app.Status -o animal_app/fixtures/initial_data/status.json
    fixtures = ["animal_app/fixtures/initial_data/status.json",]
    
    def setUp(self):
        # the unittest way of defining fixtures
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    # The individual tests are defined with methods whose names start with the 
    # letters test. This naming convention informs the test runner about which methods 
    # represent tests.
    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
```

The default behavior of the test utility is to find all the test cases (that is, subclasses of unittest.TestCase) in
any file whose name begins with test, automatically build a test suite out of those test cases, and run that suite.

### Django models in tests

If your tests rely on database access such as creating or querying models, be sure to create your test classes as 
subclasses of **django.test.TestCase** rather than **unittest.TestCase**.

### Test execution order

Using unittest.TestCase avoids the cost of running each test in a transaction and flushing the database, but if your
tests interact with the database their behavior will vary based on the order that the test runner executes them. This
can lead to unit tests that pass when run in isolation but fail when run in a suite.

### Command Line

Similarly to what happens with unittest, Django allows the same functionality where a module can be used from the 
command line to run tests from modules, classes or even individual test methods.

The example below show how tests can be executed from the most general, which runs all the tests, to the most 
particular, where only one individual test is executed.

```bash
python manage.py test
python manage.py test animal_app.tests.AnimalTestCase
python manage.py test animal_app.tests.AnimalTestCase.test_animals_can_speak
```

#### Preserve database between test execution

The test **--keepdb** option preserves the test database between test runs. It skips the create and destroy actions 
which can greatly decrease the time to run tests.

```bash
python manage.py test --keepdb
```

#### Automatically recover from a test run that was forcefully interrupted

If a test run is forcefully interrupted, the test database may not be destroyed. On the next run, you’ll be asked 
whether you want to reuse or destroy the database. Use the test **--noinput** option to suppress that prompt and 
automatically destroy the database. This can be useful when running tests on a continuous integration server where 
tests may be interrupted by a timeout, for example.

```bash
python manage.py test --noinput
```

