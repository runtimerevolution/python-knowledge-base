# Project Setup Guide 🐍

This is a short guide with the best practices, getting you up and running as programmer working with python.

*This guide was intended for macOS using the "old" **Intel x86 Processors**, if you're living on the edge with the 
new Apple M1 Chip you might run into trouble trying to follow these steps.*

## Index

- [Pyenv](#pyenv)
  - [Install](#install)
  - [Commands](#commands)
- [Virtualenv](#virtualenv)
- [Main Packages](#main-packages)
  - [Web framework](#web-framework)
  - [Linter](#linter)
  - [Auto formatter](#auto-formatter) 
- [Optional Packages](#optional-packages)
  - [Django debug toolbar](#django-debug-toolbar)
  - [Factory Boy](#factory-boy)
  - [djangorestframework](#djangorestframework)
  - [Pandas](#pandas)
---
## Pyenv

pyenv is a very handy version management system for python. You might be familiar with `nvm` if you worked with Node.js
or `rvm` if you worked with Ruby before.

Checkout the pyenv project on gitHub:

<https://github.com/pyenv/pyenv>

> pyenv lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX 
> tradition of single-purpose tools that do one thing well.

### Install

Depending on your current setup installation may vary, so I would recommend following the official installation
guide [here](https://github.com/pyenv/pyenv#installation), but you can follow along if you have the following 
prerequisites:

- [Homebrew](https://brew.sh/)
- [oh-my-zsh](https://ohmyz.sh/)

If you haven't done so, install Xcode Command Line Tools.

```shell
xcode-select --install
```

Install the Python build dependencies.

```shell
brew install openssl readline xz zlib postgresql
```

Now install pyenv with Homebrew.

```shell
brew update
brew install pyenv
```


### Commands

Let's go over some of the most important pyenv commands. You can check the full list
[here](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md)

Test if you have pyenv correctly installed by checking pyenv version in my case I have version `1.2.21` but that's 
not that important.

```shell
$ pyenv -v
pyenv 2.2.3
```

Lists all Python versions known to pyenv, and shows an asterisk next to the currently active version.

```shell
$ pyenv versions
* system (set by /Users/Roberto/.pyenv/version)
```

To list the all available versions of Python. (You're probably only interested in the versions at the top without a 
name)

```shell
pyenv install --list
```

Install a Python version

```shell
pyenv install 3.10.2
```

Sets the global version of Python to be used in all shells by writing the version name to the `~/.pyenv/version` 
file. This version can be overridden by an application-specific `.python-version` file, or by setting the 
`PYENV_VERSION` environment variable.

```shell
pyenv global 3.10.2
```

Sets a local application-specific Python version by writing the version name to a `.python-version` file in the 
current directory. This version overrides the global version, and can be overridden itself by setting the 
`PYENV_VERSION` environment variable or with the `pyenv shell` command.

```shell
pyenv local 3.10.2
```
---

## Virtualenv

[virtualenv](https://virtualenv.pypa.io/en/latest/) is a tool to create isolated Python environments.
Depending on your type of projects it is good practice having different environments for different projects

install virtualenv
```shell
python -m pip install virtualenv
```

create your virtualenv using the installed python above
```shell
pyenv virtualenv 3.10.2 your-env-or-project-name
```

activate your virtualenv
```shell
source ~/.pyenv/versions/your-env-or-project-name/bin/activate
```

optionally you can configure your terminal to always start with your environment activated, this is helpful for 
development. To do that simply add the previous command to your `.zshrc` or `.bashrc`

---
## Main Packages

### Web framework

Your web framework, we are using [django](https://docs.djangoproject.com/en/), when using the documentation make sure 
you have the right version selected on the bottom lower right corner
```shell 
python -m pip install django
```

### DB Package

[psycopg2-binary](https://pypi.org/project/psycopg2-binary/) is a package to interact with the DB

```shell
python -m pip install psycopg2-binary
```
### Linter
For linting we are using [flake8](https://flake8.pycqa.org/en/latest/). Some projects also use 
[pylint](https://pylint.org/)

What is a linter? is a tool that analyzes source code to flag programming errors, bugs, stylistic errors, and 
suspicious constructs.
```shell
python -m pip install flake8
```
### Auto formatter

> You can have any colour, as long as it's black

[Black](https://pypi.org/project/black/) is the auto-formatter chosen. It is important that the team uses the same 
auto-formatter, so the code does not keep changing on different branches because of the developer default formatter IDE.
```shell
python -m pip install black
```
Read more [here](https://black.readthedocs.io/en/stable/integrations/editors.html) about how to configure black on your
IDE, also sometimes we add the flag `--line-length 120` 
---

## Optional Packages

These packages can be skipped as your on onboard might not use/require these libraries.

### Django debug toolbar
[Django debug toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#process)
The Django Debug Toolbar is a configurable set of panels that display various debug information about the current 
request/response and when clicked, display more details about the panel's content.

The most used case for this package, is to check how many queries are performed on a list request, either by a view or 
the api. And to know when we need to implement select_related or prefetch related

In [panels](https://django-debug-toolbar.readthedocs.io/en/latest/panels.html#third-party-panels), you can find some
extra information. Check the Third-party panels, for example 
[pimpler](https://django-debug-toolbar.readthedocs.io/en/latest/panels.html#pympler) is useful to find memory usage

### Factory Boy
[Factory Boy](https://factoryboy.readthedocs.io/en/stable/)
Very useful for making tests setup simpler


### djangorestframework

[Django REST framework](https://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web 
APIs.
```shell
python -m pip install djangorestframework
python -m pip install markdown
python -m pip install django-filter
```

### Pandas
[Pandas](https://pandas.pydata.org/getting_started.html) is a fast, powerful, flexible and easy to use open source 
data analysis and manipulation tool,
built on top of the Python programming language.
```shell
python -m pip install pandas
```