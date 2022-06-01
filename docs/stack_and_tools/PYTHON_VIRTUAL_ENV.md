# Python Virtual Environment

The virtual environment ecosystem is composed by 3 different parts:

- __Python version__ Depending on the system you're using, a particular Python version can be installed via that system package manager or via `pyenv`.
- __Virtual Environment__ A virtual environment is a Python environment such that the Python interpreter, libraries and scripts installed into it are isolated from those installed in other virtual environments, and (by default) any libraries installed in a “system” Python, i.e., one which is installed as part of your operating system. [docs.python.org](https://docs.python.org/3/library/venv.html#:~:text=A%20virtual%20environment%20is%20a,part%20of%20your%20operating%20system.)
- __Dependency management__ A list of all the Python dependencies for a given project.Typically called `requirements.txt`, but can also take a more complex form where there's a distinction between which dependencies belong to production and which belong to development/testing.

---

## Python version

The most popular option is `pyenv`, even when a particular version is available in the OS package manager

### pyenv

Check the documentation at <https://github.com/pyenv/pyenv> .

Allows to specify a particular Python version to be used in a virtual environment.

List all Python versions available to pyenv

```bash
pyenv install -l
```

Choose a version and install it

```bash
pyenv install 3.10.4
```

Versions are available under are available under `~/.pyenv/versions/`

#### Global

The global command sets the global Python version, which is useful for
ensuring a particular Python version by default. If you wanted to use 3.7.10 by default,
then you could run this:

```bash
pyenv global 3.7.10
```

This command sets the ~/.pyenv/version to 3.7.10.

#### Local

The local command is used to set an application-specific Python version

```bash
pyenv local 3.10.4
```

This command creates a .python-version file in your current directory. If you have pyenv active in your environment,
this file will automatically activate this version for you.

---

## Virtual Environment

### venv

The most simple is `venv` using the Python system version

```bash
python -m venv simple-venv
```

| activate                           | deactivate   |
|------------------------------------|--------------|
| `source simple-venv/bin/activate`  | `deactivate` |

### Pyenv + Virtualenv

Pyenv supports the creation of a virtualenv tied to a particular Python version.

```bash
pyenv virtualenv 3.10.4 sample-virtual-env
```

| activate                                                   | deactivate    |
|------------------------------------------------------------|---------------|
| `source ~/.pyenv/versions/sample-virtual-env/bin/activate` | `deactivate`  |
| `pyenv local sample-virtual-env`                           | `deactivate`  |

### Poetry

This is a packaging and dependency management all in one, which means:

- it supports builds
- you can publish your package to both public and private repositories
- includes a virtualenv <https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment>.

Check the documentation available at <https://python-poetry.org/docs/>, the installation should be system-wide,
even though it can be installed on a particular environment.

```bash
poetry new poetry-demo
```

This will create the `poetry-demo` directory with the following content.

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

#### Poetry + pyenv

To use poetry with a particular Python version, that version only needs to be available in the system. In this case,
we're using a Python version provided by `pyenv`. For further documentation please
check <https://python-poetry.org/docs/managing-environments/#switching-between-environments>

```bash
cd poetry-demo
poetry env use ~/.pyenv/versions/3.10.4/bin/python
```

---

## Dependency Management

|               | pip                          | pipenv                                | Poetry                             |
|---------------|------------------------------|---------------------------------------|------------------------------------|
| search        | pip search <package_name>    | pipenv search <package_name>          | poetry search <package_name>       |
| install       | pip install <package_name>   | pipenv install <package_name>         | poetry add <package_name>          |
| install dev   |                              | pipenv install <package_name> --dev   | poetry add <package_name> --dev    |
| uninstall     | pip uninstall <package_name> | pipenv uninstall <package_name>       | poetry remove <package_name>       |
| uninstall dev |                              | pipenv uninstall <package_name> --dev | poetry remove <package_name> --dev |
| list packages | pip list                     | pip list                              | poetry show                        |
| build         |                              |                                       | poetry build                       |
| publish       |                              |                                       | poetry publish                     |

### Pip

<https://pip.pypa.io/en/stable/>

Pip is the package installer for Python. You can use it to install packages from the Python Package Index
and other indexes.

> Pip is available by default

#### Requirements.txt

> Even though this is the most common way of sharing project dependencies, it is not the greatest, since there is no
> distinction between production and development packages.

Can be generated by running

```bash
pip freeze > requirements.txt
```

### pipenv

<https://pipenv.pypa.io/en/latest/>

Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the
Python world. Windows is a first-class citizen, in our world.
It automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your Pipfile
as you install/uninstall packages. It also generates the ever-important Pipfile.lock, which is used to produce
deterministic builds.
Pipenv uses Pipfile and Pipfile.lock to separate abstract dependency declarations from the last tested combination.

#### Install

> Before proceed with the installation, please make sure the virtual environment of your choice is active

```bash
pip install pipenv
```

#### Pipfile and Pipfile.lock

__Pipfile__ holds the settings used in the project, below there's a list most common ones:

- source: python package repository, by default is set to pypi
- dev-packages: list of _development_ packages and macthing version defined by the user, which is * if not specified
- packages: list of _production_ packages and matching version defined by the user, which is * if not specified
- requires: python version of the project

> Even though pipfile allows for a package to be installed without a particular version being set, this is not
>advisable, since it will take longer to determine the best version to be installed. This is mostly noticed when
> the project has a lot of packages.

__Pipfile.lock__ holds the exact version that was installed upon the time of the version lock. As an example, lets say
we're using Django but haven't set a particular version, this means everytime we run `pipenv install` the latest
version of Django would be installed.

### Poetry dependency management

<https://python-poetry.org/docs/dependency-specification/>

Simillarly to Pipenv, Poetry also allows a version lock and a distinction between production and development packages.

- tool.poetry.dependencies: list of _production_ packages and matching version defined by the user, which is * if not
specified. Python version is also specified here
- tool.poetry.dev-dependencies: list of _development_ packages and matching version defined by the user, which is * if
not specified

### pipx

<https://pypa.github.io/pipx/>

Pipx allows the installation and execution of Python applications in isolated environments. It's not recommended to use
within a project, but very suitable for running standalone python applications.
