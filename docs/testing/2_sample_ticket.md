# Sample Ticket

Let's take a hypothetical ticket where we're required to create a very simple
report generator.  

## Report Generator

### Requirements

Develop the necessary functionality to create a report generator using
[Jinja2](https://jinja.palletsprojects.com/en/3.1.x/). 
This report must take as parameters: 

 - __title__: string with the title of the report
 - __description__: string with the description of the report
 - __data__: string generated from a [pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

The template must follow the structure below

```html
Report

{{title}}

{{description}}

{{data}}
```

### Acceptance Criteria

- Must follow the following code principles
  
    - [Don't repeat yourself (DRY)](../best_practices/code_principles.md#dry-dont-repeat-yourself-2)
    - [Single-responsibility principle (SRP)](../best_practices/code_principles.md#single-responsibility-principle-srp)

- Must include unit test

### Sample Report

```text
Report

Very Important Report

Sample description

   col1  col2
0     1     3
1     2     4
```

## Initial approach

In our initial approach we're simple playing around with Jinja2, to make
sure we can build what we're required. After a quick look into the Jinja2
[documentation](https://jinja.palletsprojects.com/en/3.1.x/nativetypes/#examples)
we come up with the following working example.

```python
from jinja2.nativetypes import NativeEnvironment
import pandas as pd

TEMPLATE = """
Sample Report

{{title}}

{{description}}

{{data}}
"""

title = "Very Important Report"
description = "Sample description"
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

env = NativeEnvironment()
template = env.from_string(TEMPLATE)
report = template.render(title=title, description=description, data=df.to_string())
print(report)
```

Which produces the following result 

```text
Report

Very Important Report

Sample description

   col1  col2
0     1     3
1     2     4
```

Even though it performs as expected, it doesn't follow the acceptance criteria.

:octicons-x-circle-16: Must follow the Don't repeat yourself (DRY) code principle

:octicons-x-circle-16: Must follow the Single-responsibility principle (SRP) code principle

:octicons-x-circle-16: Must include unit test
 
## Turn it into a function

After concluding that the acceptance criteria isn't met, we quickly conclude
that a function might do the trick.

```python
from jinja2.nativetypes import NativeEnvironment
import pandas as pd

TEMPLATE = """
Report

{{title}}

{{description}}

{{data}}
"""

title = "Very Important Report"
description = "Sample description"
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

def generate_report(title, description, data):
    env = NativeEnvironment()
    template = env.from_string(TEMPLATE)
    return template.render(title=title, descritpion=description, data=data)

generate_report(title, description, df.to_string())
```

Time to test it! Since [Unitest](https://docs.python.org/3/library/unittest.html)
is the default Unit testing framework in Python, we'll use it in this exercise.

```python
import unittest
from unittest import TestCase

class GenerateReportTest(TestCase):
    def test_success(self):
        title = "sample title"
        description = "sample description"
        data = "42"

        report = generate_report(title, description, data)
        self.assertTrue(title in report)
        self.assertTrue(description in report)
        self.assertTrue(data in report)
        
    def test_failure(self):
        generate_report(None, None, None)

if __name__ == '__main__':
    unittest.main()
```

The TestCase includes two tests, one for the case we consider to be a __success__ and
another for the case we consider to be a __failure__. 

The __success__ asserts that whatever that was used to generate a report is present in it.

On the other hand, the __failure__ asserts by means of a successful execution that is possible
to generate an empty report.

## Validations galore

Time to ensure that whatever report we generate is meaningful, which means we need to validate our three
parameters.

Since we need all three to exist, let's add the following snippet which breaks if at least one
of them is `None`.

```python
if title is None or description is None or data is None:
    return
```

The updated generate report function. 

```python
def generate_report(title, description, data):
    if title is None or description is None or data is None:
        return
    env = NativeEnvironment()
    template = env.from_string(TEMPLATE)
    return template.render(title=title, description=description, data=data)
```

The existing tests should pass as they are, however we should improve the __failure__ test. Now
we want to assert that if at least one of the parameters is `None`, the response is `None` as
well.

```python
import unittest
from unittest import TestCase

class GenerateReportTest(TestCase):
    def setUp(self):
        self.title = "sample title"
        self.description = "sample description"
        self.data = "42"

    def test_success(self):
        report = generate_report(self.title, self.description, self.data)
        self.assertTrue(self.title in report)
        self.assertTrue(self.description in report)
        self.assertTrue(self.data in report)

    def test_failure_1_params(self):
        self.assertIsNone(generate_report(self.title, None, self.data))

    def test_failure_3_params(self):
        self.assertIsNone(generate_report(None, None, None))

if __name__ == '__main__':
    unittest.main()
```

Since `title`, `description` and `data` are used in two different tests they're added to
[setUp](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp) method.

---

After grouping the logic in a function, adding parameters validation and tests, it's time to
revisit the [Acceptance criteria](#acceptance-criteria). 


:fontawesome-solid-circle-check: Must follow the Don't repeat yourself (DRY) code principle

:octicons-x-circle-16: Must follow the Single-responsibility principle (SRP) code principle, the `generate_report` functions is doing
all the work, the validation and the generation of the report.

:fontawesome-solid-circle-check: Must include unit test

## Set responsibilities

Instead of having a function for validation and another for generation, we're going to create a class
to handle the generation of the report.

```python
import pandas as pd
from jinja2.nativetypes import NativeEnvironment
from dataclasses import dataclass

TEMPLATE = """
Report

{{title}}

{{description}}

{{data}}
"""

title = "Very Important Report"
description = "Sample description"
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

@dataclass
class GenerateReport:
    title: str
    description: str
    data: str

    def __post_init__(self):
        self._validate_input()
        self._get_template()

    def _validate_input(self):
        if self.title is None or self.description is None or self.data is None:
            raise Exception("Parameters are missing")

    def _get_template(self):
        env = NativeEnvironment()
        self.template = env.from_string(TEMPLATE)

    def __call__(self, *args, **kwargs):
        return self.template.render(title=self.title, description=self.description, data=self.data)

generate_report = GenerateReport(title, description, df.to_string())
print(generate_report())
```

Let's update the tests to follow up on the changes we've just performed.

```python
import unittest
from unittest import TestCase

class GenerateReportTest(TestCase):
    def setUp(self):
        self.title = "sample title"
        self.description = "sample description"
        self.data = "42"

    def test_success(self):
        report = GenerateReport(self.title, self.description, self.data)()
        self.assertTrue(self.title in report)
        self.assertTrue(self.description in report)
        self.assertTrue(self.data in report)

    def test_failure_1_params(self):
        report = GenerateReport(self.title, None, self.data)()
        self.assertIsNone(report)

    def test_failure_3_params(self):
        report = GenerateReport(None, None, None)()
        self.assertIsNone(report)

if __name__ == '__main__':
    unittest.main()
```

However the tests are now failing

```text
test_failure_1_params (__main__.GenerateReportTest) ... ERROR
test_failure_3_params (__main__.GenerateReportTest) ... ERROR
test_success (__main__.GenerateReportTest) ... ok
```

What changed? Previously we're just returning `None` 

```python
if title is None or description is None or data is None:
    return
```

while now, we're raising and exception

```python
def _validate_input(self):
    if self.title is None or self.description is None or self.data is None:
        raise Exception("Parameters are missing")
```

Let's update the tests to follow on that update


```python
import unittest
from unittest import TestCase

class GenerateReportTest(TestCase):
    def setUp(self):
        self.title = "sample title"
        self.description = "sample description"
        self.data = "42"

    def test_success(self):
        report = GenerateReport(self.title, self.description, self.data)()
        self.assertTrue(self.title in report)
        self.assertTrue(self.description in report)
        self.assertTrue(self.data in report)

    def test_failure_1_params(self):
        with self.assertRaises(Exception) as cm:
            GenerateReport(self.title, None, self.data)()

        self.assertEqual(cm.exception.args[0], "Parameters are missing")

    def test_failure_3_params(self):
        with self.assertRaises(Exception) as cm:
            GenerateReport(None, None, None)()

        self.assertEqual(cm.exception.args[0], "Parameters are missing")

if __name__ == '__main__':
    unittest.main()
```

What if the report variables change? How many changes are necessary to perform in our code?

Now we're clearly following the single-responsibility principle, but is there room for improvement? If something fails
in the validation, we don't know for sure what failed so let's add that.

Instead of having a very simple validation, such as

```python
def _validate_input(self):
    if self.title is None or self.description is None or self.data is None:
        raise Exception(f"Parameters are missing")
```

What's changing:

- we're replacing all the class parameters by a dictionary
- we're setting all the expected template variables to have a reference of what is expected 

```python
data: dict
TEMPLATE_VARIABLES: ClassVar[set] = {"title", "description", "data"}

def _validate_input(self):
    missing = set(self.data.keys()) ^ self.TEMPLATE_VARIABLES
    if missing:
        raise Exception(f"The following keys are missing: {missing}")
```

Here's our updated class for the report generator.

```python
import pandas as pd

from jinja2.nativetypes import NativeEnvironment
from typing import ClassVar
from dataclasses import dataclass

TEMPLATE = """
Report

{{title}}

{{description}}

{{data}}
"""

title = "Very Important Report"
description = "Sample description"
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

data = {"title": title, "description": description, "data": df.to_string()}

@dataclass
class GenerateReport:
    data: dict
    TEMPLATE_VARIABLES: ClassVar[set] = {"title", "description", "data"}

    def __post_init__(self):
        self._validate_input()
        self._get_template()

    def _validate_input(self):
        missing = set(self.data.keys()) ^ self.TEMPLATE_VARIABLES
        if missing:
            raise Exception(f"The following keys are missing: {missing}")

    def _get_template(self):
        env = NativeEnvironment()
        self.template = env.from_string(TEMPLATE)

    def __call__(self, *args, **kwargs):
        return self.template.render(**self.data)

report = GenerateReport(data)()
print(report)
```

And let's add a test for it 

```python
import unittest
from unittest import TestCase

class GenerateReportTest(TestCase):
    def setUp(self):
        self.title = "sample title"
        self.description = "sample description"
        self.data = "42"

        self.template_data = {"title": self.title,
        "description": self.description,
        "data": self.data}

    def test_success(self):
        report = GenerateReport(self.template_data)()
        self.assertTrue(self.title in report)
        self.assertTrue(self.description in report)
        self.assertTrue(self.data in report)

    def test_failure_1_params(self):
        self.template_data.pop('description')
        with self.assertRaises(Exception) as cm:
            GenerateReport(self.template_data)()

        self.assertEqual(
            cm.exception.args[0],
            "The following keys are missing: {'description'}")

    def test_failure_3_params(self):
        with self.assertRaises(Exception) as cm:
            GenerateReport({})()

        self.assertEqual(
            cm.exception.args[0],
            "The following keys are missing: {'title', 'description', 'data'}")

if __name__ == '__main__':
    unittest.main()
```
