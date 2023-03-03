# Coverage

<https://coverage.readthedocs.io/>

Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not. Coverage.py won't fix anything in your code but will show you parts of your code that aren't being tested.

This guide will show you how to run coverage.py and generate a final report in html.

## Running coverage

After installing, running coverage on your test suite is as simple as calling the following command:

```bash
coverage run manage.py test
```

This will seemingly run your tests and do nothing else, but it will create a .coverage file in the current working directory. You can open that file but it will be complicated to read anything, run the command `coverage report` to see the results.

## Better output

You can just do a `coverage run` and then a `coverage report` or you can have something better like storing the results in an html file and then open it in the browser. To do this, instead of running `coverage report`, you can run:

```bash
coverage html --skip-empty
```

This will generate a folder called htmlcov. Inside that folder, you will see a lot of files, mainly the index.html file; if you open this file, you will see a much better result.

The flag `--skip-empty` will skip empty files. For example, empty "__init__.py" files won't be included in the html report because you don't need that kind of noise in your report.

## Ignoring folders, files or code

To ignore code that you don't want to be tested, you can create a file called ".coveragerc" in the same directory you will be running coverage. Here's an example:

```text
[run]
omit =
    */tests/*
    folder1/*
    folder2/*
    folder3/*
    path/to/file/the_file.py
    if self.debug:
    if settings.DEBUG
```

This example will do the following:

- "\*/tests/\*": Ignore any directory called "tests" in the project structure and its contents;
- "folder1/\*", "folder2/\*", "folder3/\*": These 3 folders and their contents will be ignored;
- "path/to/file/the_file.py": Ignore any directory called "tests" in the project structure and its contents;
- `if self.debug:` and `if settings.DEBUG`: The line itself and everything inside its scope will be ignored;

## Complete example for Django project using Make

With coverage installed and the .coveragerc file defined, you can use this make command to run your tests, generate and open an html report:

```make
test_with_report:
    cd tutorial && coverage run manage.py test && coverage html --skip-empty --skip-covered
    open tutorial/htmlcov/index.html
```

This will get your basics covered. It will run your tests through coverage, then it will generate an html report where it skips empty files and files where you have 100% coverage, and finally it will open the generated html report in your browser.

## Final note

This doesn't work with pytest. For pytest, you need something called [pytest-cov](https://pytest-cov.readthedocs.io/).

## Documentation

You can and should check the documentation [here](https://coverage.readthedocs.io) so you can see all that is possible with the coverage.py tool.
