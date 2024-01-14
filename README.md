# PyTeleBetter
## Introduction
A refactoring and cleanup of a really old project of mine. 
PyTeleBetter is an app that allows to automatically reply to the posts in Telegram channels. It aims to be powerful and simple to use. 

### Features
- Multi-account
- Multi-channel
- Automatic account setup
- Automatic channel for account setup (not tested as i don't have a premium account, but it worked in the past.)

## Installation
```sh
git clone https://github.com/InvincibleDude/PyTeleBetter/
poetry install
poetry run main
```
## Configuration
In `config_accounts.json.example` file there is an example of how to setup an account for this tool.
There are two reply modes - `peg` and `py`. The latter is unrecommended and untested, as it poses a security risk. 
The `peg` mode is able to randomize your messages by using a simple template language. You can look at an example of it in the provided example config file. You can add as many variations as you can, by separating them with `|`, but you can't nest the variations.
The images for the channel layer setup are put in the images folder and their names must follow the following template:
```python
# (all|{index}) - chooses a photos that are assigned to all (0) or to specific account ({index})
# (pfp|clp|ptsw):
#   pfp - profile picture
#   clprofile - channel layer profile picture
#   clpost - channel layer profile post pics
# ([0-9]) - index of photo
# Examples: 0_ptsw_1.png, 0_ptsw_2.jpg
```
