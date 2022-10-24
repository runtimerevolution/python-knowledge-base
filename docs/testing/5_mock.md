# unittest.Mock

> this document was inspired/copied from of [https://docs.python.org/3/library/unittest.mock.html](https://docs.python.org/3/library/unittest.mock.html)

`unittest.mock` is a library for testing in Python. It allows you to replace parts of your system under test with mock
objects and make assertions about how they have been used.

> Mock an item where it is used, not where it came from.

Let's consider the following example, where there's a function that returns yesterday's date.

```python
# utils.py
from django.utils import timezone
from datetime import timedelta


def yesterday():
    dt = timezone.now() + timedelta(days=-1)
    return dt.date()

```

Let's compare the equivalent approaches we can have for that code sample.

## Mock

Mock is a flexible mock object intended to replace the use of stubs and test doubles throughout your code. Mocks are callable and create attributes as new mocks when you access them. Accessing the same attribute will always return the same mock. Mocks record how you use them, allowing you to make assertions about what your code has done to them.

```python
from datetime import datetime

from django.test import TestCase

from ..utils import yesterday, timezone
from unittest.mock import Mock

class YesterdayTestMock(TestCase):

    def test_success(self):
        """
        Mock an item where it is used, not where it came from.
        In this case even though timezone in utils.py is imported
        from django.utils, we want to mock timezone from utils.
        """
        tz = timezone
        tz.now = Mock(return_value=datetime(1945, 2, 12, 0, 0, 0))

        expected = datetime(1945, 2, 11).date()

        self.assertEqual(yesterday(), expected)

```

## MagicMock

MagicMock is a subclass of Mock with all the magic methods pre-created and ready to use. There are also non-callable variants, useful when you are mocking out objects that aren’t callable: NonCallableMock and NonCallableMagicMock.

```python
from datetime import datetime

from django.test import TestCase

from ..utils import yesterday, timezone
from unittest.mock import MagicMock


class YesterdayTestMagicMock(TestCase):

    def test_success(self):
        """
        Mock an item where it is used, not where it came from.
        In this case even though timezone in utils.py is imported
        from django.utils, we want to mock timezone from utils.
        """
        tz = timezone
        tz.now = MagicMock(return_value=datetime(1945, 2, 12, 0, 0, 0))

        expected = datetime(1945, 2, 11).date()

        self.assertEqual(yesterday(), expected)
```

## Patch

The `patch()` decorators makes it easy to temporarily replace classes in a particular module with a Mock object. By default patch() will create a MagicMock for you. You can specify an alternative class of Mock using the new_callable argument to patch().

```python
from datetime import datetime

from django.test import TestCase

from ..utils import yesterday
from unittest.mock import patch

class YesterdayTest(TestCase):

    @patch("library.utils.timezone.now")
    def test_success(self, mock):
        """
        Mock an item where it is used, not where it came from.
        In this case even though timezone in utils.py is imported
        from django.utils, we want to mock timezone from utils.
        """
        mock.return_value = datetime(1945, 2, 12, 0, 0, 0)

        expected = datetime(1945, 2, 11).date()

        self.assertEqual(yesterday(), expected)
```

## Side effect

This can either be a function to be called when the mock is called, an iterable or an exception (class or instance) to be raised.

An example of a mock that raises an exception (to test exception handling of an API):

```python
>>>mock = Mock()
>>>mock.side_effect = Exception('Boom!')
>>>mock()
Traceback (most recent call last):
  ...
Exception: Boom!
```

Using side_effect to return a sequence of values:

```python
>>>mock = Mock()
>>>mock.side_effect = [3, 2, 1]
>>>mock(), mock(), mock()
(3, 2, 1)
```

Setting side_effect to None clears it:

```python
>>>mock = Mock(side_effect=KeyError, return_value=3)
>>>mock()
Traceback (most recent call last):
 ...
KeyError
>>>mock.side_effect = None
>>>mock()
3
```

## Asserts

### assert_called()

Assert that the mock was called at least once.

```python
>>>mock = Mock()
>>>mock.method()
<Mock name='mock.method()' id='...'>
>>>mock.method.assert_called()
```

### assert_called_once()

Assert that the mock was called exactly once.

```python
>>>mock = Mock()
>>>mock.method()
<Mock name='mock.method()' id='...'>
>>>mock.method.assert_called_once()
>>>mock.method()
<Mock name='mock.method()' id='...'>
>>>mock.method.assert_called_once()
Traceback (most recent call last):
...
AssertionError: Expected 'method' to have been called once. Called 2 times.
```

### assert_called_with(*args, **kwargs)

This method is a convenient way of asserting that the last call has been made in a particular way:

```python
>>>mock = Mock()
>>>mock.method(1, 2, 3, test='wow')
<Mock name='mock.method()' id='...'>
>>>mock.method.assert_called_with(1, 2, 3, test='wow')
```

### assert_called_once_with(*args, **kwargs)

Assert that the mock was called exactly once and that call was with the specified arguments.

```python
>>>mock = Mock(return_value=None)
>>>mock('foo', bar='baz')
>>>mock.assert_called_once_with('foo', bar='baz')
>>>mock('other', bar='values')
>>>mock.assert_called_once_with('other', bar='values')
Traceback (most recent call last):
    ...
AssertionError: Expected 'mock' to be called once. Called 2 times.
```

### assert_any_call(*args, **kwargs)

Assert the mock has been called with the specified arguments.

The assert passes if the mock has ever been called, unlike `assert_called_with()` and `assert_called_once_with()` that only pass if the call is the most recent one, and in the case of `assert_called_once_with()` it must also be the only call.

```python
>>>mock = Mock(return_value=None)
>>>mock(1, 2, arg='thing')
>>>mock('some', 'thing', 'else')
>>>mock.assert_any_call(1, 2, arg='thing')
```

### assert_has_calls(calls, any_order=False)

Assert the mock has been called with the specified calls. The mock_calls list is checked for the calls.

If any_order is false then the calls must be sequential. There can be extra calls before or after the specified calls.

If any_order is true then the calls can be in any order, but they must all appear in mock_calls.

```python
>>>mock = Mock(return_value=None)
>>>mock(1)
>>>mock(2)
>>>mock(3)
>>>mock(4)
>>>calls = [call(2), call(3)]
>>>mock.assert_has_calls(calls)
>>>calls = [call(4), call(2), call(3)]
>>>mock.assert_has_calls(calls, any_order=True)
```

### assert_not_called()

Assert the mock was never called.

```python
>>>m = Mock()
>>>m.hello.assert_not_called()
>>>obj = m.hello()
>>>m.hello.assert_not_called()
Traceback (most recent call last):
    ...
AssertionError: Expected 'hello' to not have been called. Called 1 times.
```

### reset_mock(*, return_value=False, side_effect=False)

The reset_mock method resets all the call attributes on a mock object:

```python
>>>mock = Mock(return_value=None)
>>>mock('hello')
>>>mock.called
True
>>>mock.reset_mock()
>>>mock.called
False
```

This can be useful where you want to make a series of assertions that reuse the same object. Note that `reset_mock()` **doesn’t clear** the return value, side_effect or any child attributes you have set using normal assignment by default. In case you want to reset return_value or side_effect, then pass the corresponding parameter as True. Child mocks and the return value mock (if any) are reset as well.
