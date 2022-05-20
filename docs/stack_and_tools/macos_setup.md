# Macbook OS Setup

- [Mac M1](#mac-m1)
- [General Setup](#general-setup)

---

## Mac M1

* Install all OS updates, via System Preferences
* Terminal
  * Iterm2 (https://iterm2.com/), an improved version of the mac terminal
  * Default Mac Terminal
* Activate Rosetta emulator (https://support.apple.com/en-us/HT211861)
  * Since the M1 Macs have a different architecture than the previous releases, there might be some incompatibility issues with some
  apps/software/libraries. To activate rosetta, do:
    1. open Finder
       1. if using iTerm2 go to Applications
       2. if using default Terminal go to Applications/Utilities
    2. right-click the terminal app of your choice and select the `Get Info` option
    3. then just click on the Checkbox that says `Open using Rosetta`
    4. restart the terminal 
    5. now your terminal can run as it would on an Apple with an Intel processor
* Install HomeBrew https://brew.sh/ from that terminal

---

## General Setup

* Install Oh My Zsh (https://ohmyz.sh/), this improves the terminal experience
  * adds custom themes, helpers, plugins etc
  * can be configured with the .zshrc file on the home folder ~/
* Migrating from another mac
  * profile export as JSON option is available on the Profile menu
* Install Homebrew (https://brew.sh/) package manager
  * easy installation of programming languages, helpers, services on the OS
  * run ``brew upgrade`` before installing any package;
* Install Docker, available at https://docs.docker.com/desktop/mac/install/
* Install DBeaver, available at https://dbeaver.io/ or install via HomeBrew https://formulae.brew.sh/cask/dbeaver-community
  * a universal database tool

