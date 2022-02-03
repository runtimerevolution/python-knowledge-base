# Macbook OS Setup

* Install all OS updates (via System Preferences);
* Install Iterm2 - an improved version of the mac terminal - https://iterm2.com/;
* Since the M1 Macs have a different architecture, there might be some imcompatiblity issues with some apps/software, to solve this we can run the terminal with the Rosetta emulator (https://support.apple.com/en-us/HT211861). To add rosetta, just right click the Iterm app and select the `Get Info` option, then just click on the Checkbox that says `Open using Rosetta`, restart the terminal and now your terminal can run as it would on an Apple with an Intel processor;
* To improve the usage of the terminal, install Oh My Zsh (https://ohmyz.sh/), this adds custom themes, helpers, plugins etc and can be configurated with the .zshrc file on ~/ folder;
* If you are migrating from another mac, you can import the profile using the export as JSON option on the Profile menu;
* After customizing the shell install Homebrew (https://brew.sh/), this is the package manager that allows for an easy installation of programming languages, helpers, services on the OS;
* Run ``brew upgrade`` before installing any package;
* Install Pyenv (https://github.com/pyenv/pyenv) to manage all python versions installations;
* For the code editor, we have the more common option:
    * VS Code - https://code.visualstudio.com/ - Lightweighted code editor with an easy customization and supports many plugins and configurations;
    * PyCharm - https://www.jetbrains.com/pycharm/ - Jetbrains IDE for python projects, has plugins and full integrations with Database viewers;
* Install docker - https://docs.docker.com/desktop/mac/install/;

### VS Code extensions

* Djaneiro - Adds snippets for django (templates for models, services, etc...);
* GitLens - Full integration with Git;
* Pylance - Adds python language support;
* Python - Enables debugging on vs code;
