# Python Virtual Environment Ecosystem

The virtual environment ecosystem is composed by 3 different parts:

-  __Python version__ Depending on the system you're using, a particular Python version can be installed via that system package manager or via `pyenv`.
- __Virtual Environment__ A virtual environment is a Python environment such that the Python interpreter, libraries and scripts installed into it are isolated from those installed in other virtual environments, and (by default) any libraries installed in a “system” Python, i.e., one which is installed as part of your operating system. [docs.python.org](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.)
- __Dependency listing__ A list of all the Python dependencies for a given project.Typically called `requirements.txt`, but can also take a more complex form where there's a distinction between which dependencies belong to production and which belong to development/testing.

---

## Python version

The most popular option is `pyenv`, even when a particular version is available in the OS package manager

### pyenv

Check the documentation at https://github.com/pyenv/pyenv .

Allows to specifiy a particular Python version to be used in a virtual environment.

List all Python versions available to pyenv

```bash
pyenv install -l
```

Choose a version and install it

```bash
pyenv install 3.10.4
```

Versions are available under are available under `~/.pyenv/versions/`

---

## Virtual Environment

### venv

The most simple for is `venv` using the Python system version

```bash
python -m venv simple-venv
```

### Pyenv + Virtualenv

Pyenv supports the creation of a virtualenv tied to a particular Python version.

```bash
pyenv virtualenv 3.10.4 sample-virtual-env
```

### Poetry

Includes a virtualenv https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment. 

Check the documentation available at https://python-poetry.org/docs/, the installation should be system wide, even though it can be installed on a particular environment.


```bash
poetry new poetry-demo
```

This will create the `poetry-demo` direcctory with the following content.

```bash
poetry-demo
├── pyproject.toml
├── README.rst
├── poetry_demo
│   └── __init__.py
└── tests
    ├── __init__.py
    └── test_poetry_demo.py
```



### Pyenv + virtualenv + pipenv




### Poetry + pyenv

To use poetry with a particular Python version, that version only needs to be available in the system. In this case, we're using the a Python version provided by `pyenv`.

```bash
cd poetry-demo
poetry env use ~/.pyenv/versions/3.10.4/bin/python
```
