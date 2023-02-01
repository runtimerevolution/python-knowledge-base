# Pre-commit

## Introduction
Git hook scripts are useful for identifying simple issues before submission to code review. We run our hooks
on every commit to automatically point out issues in code such as missing semicolons, trailing whitespace,
and debug statements. By pointing these issues out before code review, this allows a code reviewer to focus
on the architecture of a change while not wasting time with trivial style nitpicks.

## Motivation

- When you forget to run a linter, and your commit fails on CI because
- When you commit a file, and the only change are the import order, because you use VScode or Pycharm, and 
the last person who changed the code uses the opposite.

## Requirements

For this pre-commit, we are assuming that you want at least flake8, isort and black in dev 
(requirements/pipenv/poetry). For your project you can
remove(although you should be using black isort and a linter) or add other checks from 
the [complete list](https://pre-commit.com/hooks.html) like:

- [type checker for python](github.com/pre-commit/mirrors-mypy)
- [docstring checker  PEP-257](https://github.com/FalconSocial/pre-commit-mirrors-pep257)
- [yaml lint](https://github.com/adrienverge/yamllint)

Assuming you are using poetry you would run something like:

```
poetry add --dev pre-commit==2.19.0
poetry add --dev flake8==3.9.2 
poetry add --dev black==22.3.0 
poetry add --dev isort==5.10.1
```

## Setup

Add a file on root named `.pre-commit-config.yaml`
```
default_language_version:
  python: python3.10
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0 # Replace by any tag/version: https://github.com/psf/black/tags
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: "5.10.1" # Use the revision sha / tag you want to point at
    hooks:
      - id: isort
        args: ["--profile", "black"]
  - repo: https://github.com/pycqa/flake8
    rev: "4.0.1"
    hooks:
      - id: flake8
```

optionally, but highly recommended, you could also add these useful checks

```
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.1.0 # Use the ref you want to point at
    hooks:
      - id: check-added-large-files
        args: ["--maxkb=1024"] # throw an error if we try to commit a 1MB or greater file
      - id: check-case-conflict # so we don't rename files that will break case insensitive filesystems
      - id: check-merge-conflict # don't accidentally commit files with incomplete merges
      - id: end-of-file-fixer # makes all files end in a newline
      - id: mixed-line-ending # fixes mixed line endings automatically
      - id: no-commit-to-branch
        args: ["--branch", "master"] # no commits to master
```

configure a `.pyproject.toml` file if you don't have one create one on root folder

```
[tool.black]
line-length = 120

[tool.isort]
profile = "black"
```

configure a `.flake8` file if you don't have one create one on root folder

```
[flake8]
max-line-length = 120
max-complexity=10
exclude =
    */migrations/*
    __pycache__
    manage.py
    settings.py
    env
    .env
    ./env
    env/
    .env/
    .venv/
    inspectdb_models
```

## Activation / Deactivation

To enable pre-commit just run:
```
pre-commit install
```
To disable pre-commit just run:
```
pre-commit uninstall
```
