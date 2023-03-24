# Performance

If the battery of tests in a project starts taking too long to complete, here's a few tips to improve performance:

# setUpTestData and setUpClass

If you have several test_ methods in your TestCase class and all of them (or most of them) are using data created in the method "setUp", you should pass that data creation to the method setUpTestData. Here's some key points about setUpTestData:

- It's not a method of unittest, but it's a django creation that was created to help speed up test execution.
- It's invoked by setUpClass. So, if you also override setUpClass to do something else, setUpTestData will only be called when you invoke the super's setUpClass.
- Will only execute once for all tests inside a TestCase class, which means you can place data creation operations there to optimize your tests performance. After running all tests, there will be a rollback for all data created in setUpTestData.
- It's a classmethod, so don't just rename setUp to setUpTestData.

Here's an example, consider this TestCase:

```python
class PostTestCase(TestCase):
    def setUp(self):
        self.url = reverse("post-url")
        self.data = {"field": "value"}
        self.model = factories.ModelFactory()

    def test_success(self):
        result = self.client.post(f"{self.url}", data=self.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual(models.Model.objects.all().count(), 2)

    def test_failure(self):
        result = self.client.post(f"{self.url}", data={})
        self.assertEqual(result.status_code, 400)
        self.assertEqual(models.Model.objects.all().count(), 1)
```

The setUp method here is not optimal because the line `self.model = factories.ModelFactory()` is going to be executed twice, meaning that it will create and destroy an object before running the first test, and then it's going to do it again for the other test (and again for all other tests in the TestCase).

Ideally, this line would only be created at the beginning of test execution and destroyed after all tests in the TestCase have ran. We can achieve this with setUpTestData like so:

```python
class PostTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = reverse("post-url")
        cls.data = {"field": "value"}

    @classmethod
    def setUpTestData(cls):
        cls.model = factories.ModelFactory()
        
    ...
```

- Note that we also used setUpClass for setting up the url and the data dictionary. This is also an optimization although a very minor one for this example. setUpClass will only run once for all tests in a TestCase class. However, there will be no rollback of data created there, so setUpClass becomes ideal for defining necessary program variables for all tests to use.
- Also note that it's necessary to call `super().setUpClass()`. TestCase's setUpClass is the one responsible for calling the setUpTestData method.
- This is merely an example to show how time can be optimized in django tests; More tests and data that is more complex will benefit much more from a correct usage of setUpClass and setUpTestData.

# SimpleTestCase vs TestCase vs TransactionTestCase

This is a simple optimization to implement. All you have to do is pay attention to the following: Do the tests in a class use the database?

If you aren't using the database, use SimpleTestCase.
If you do need the database, then consider the following: Do any of your tests actually need to test any database transaction-related behavior?
If the answer is no or you are unsure, the answer is in most cases, use TestCase.
If you need to test specific database behavior when you're commiting data, use TransactionTestCase.

This is an important distintion to understand. TestCase makes use of database transactions to speed up tests. This means that within a test method, any database modifications are only visible to that test and aren't actually committed to the database. If you use the --keepdb flag, run a test (that uses TestCase), and use an external tool to inspect the test database, you won't find the changes that a test in a TestCase makes.

[Django's documentation on TestCase and TransactionTestCase](https://docs.djangoproject.com/en/4.1/topics/testing/tools/#testcase) is excellent and further explains what's going.

# Flags

When invoking django's test suite, there's a few flags that you can use locally to not only improve performance, but also make the execution more convenient:

- --parallel x: Where x is the number of threads you want to launch for parallel execution of your tests. If you want to use this flag consistently, you should consider it a last resource. First, try to optimize your tests to have better performance (If time allows) and after all has been optimized, you can use this flag more freely.
- --keepdb: This flag will persist your test database and will skip creating/destroying the database when you invoke the test suite.
- --failfast: This flag is particularly useful when you want to make sure your tests are running locally and you don't want to wait for all of them to execute. As soon as a test fails, the test suite execution will be aborted, and you can start analyzing why the test failed and fix it. This is becomes more and more useful, the longer your tests take to run.
