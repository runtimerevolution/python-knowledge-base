# Python Setup Guide 🐍

This is a short guide with the best practices to get you up and running as programmer working with python.

*This guide was intended for macOS using the "old" **Intel x86 Processors**, if you're living on the edge with the new Apple M1 Chip you might run into trouble trying to follow these steps.*

## pyenv

pyenv is a very hand version management system for python. You might be familiar with `nvm` if you worked with Node.js or `rvm` if you worked with Ruby before.

Checkout the pyenv project on github:

<https://github.com/pyenv/pyenv>

> pyenv lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.

### Install

Depending on your current setup installation may vary so I would recommend following the the official installation guide [here](https://github.com/pyenv/pyenv#installation) but you can follow along if you have the following prerequisites:

- [Homebrew](https://brew.sh/)
- [oh-my-zsh](https://ohmyz.sh/)

If you haven't done so, install Xcode Command Line Tools.

```shell
xcode-select --install
```

Install the Python build dependencies.

```shell
brew install openssl readline sqlite3 xz zlib
```

Now install pyenv with Homebrew.

```shell
brew update
brew install pyenv
```

Then add pyenv to your list of plugins on your `~/.zshrc` file, reload your shell and you're done.

```sh
plugins=(git pyenv)
```

*NOTE: elements in zsh arrays are separated by whitespace (spaces, tabs, newlines...). DO NOT use commas.*

### Commands

Let's go over some of the most important pyenv commands. You can check the full list [here](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md)

Test if you have pyenv correctly installed by checking pyenv's version in my case I have version `1.2.21` but that's not that important.

```shell
$ pyenv -v
pyenv 1.2.21
```

Lists all Python versions known to pyenv, and shows an asterisk next to the currently active version.

```shell
$ pyenv versions
* system (set by /Users/Roberto/.pyenv/version)
```

To list the all available versions of Python. (You're probably only interested in the versions at the top without a name)

```shell
pyenv install --list
```

Install a Python version

```shell
pyenv install 3.10.2
```

Sets the global version of Python to be used in all shells by writing the version name to the `~/.pyenv/version` file. This version can be overridden by an application-specific `.python-version` file, or by setting the `PYENV_VERSION` environment variable.

```shell
pyenv global 3.10.2
```

Sets a local application-specific Python version by writing the version name to a `.python-version` file in the current directory. This version overrides the global version, and can be overridden itself by setting the `PYENV_VERSION` environment variable or with the `pyenv shell` command.

```shell
pyenv local 3.10.2
```
