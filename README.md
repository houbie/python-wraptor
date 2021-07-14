# Python wraptor

CLI wrapper for automatic installation of Python tools:
* Make it be a breeze for others to get started with your project
* Get reproducible builds by always using the correct versions of your build tools
* Plays well with build tools like [Poetry](https://python-poetry.org/) and [PDM](https://pdm.fming.dev/)

![velociraptor](docs/velociraptor.png)

## Installation
No tools to install 😍

![Cast](./docs/poetry-build-cast.svg)

Copy _pw_ and _pw.bat_ to your project's root folder and add it under version control.

Having _python3_ (or _python_ on Windows) >= 3.6 and _pip3_ available on your path is the only prerequisite.

## Configuration
Add the _tool.wraptor_ section inside _pyproject.toml_ in your project's root folder.

Each entry has the form 

`tool = "pip install arguments"`

Example:
```toml
[tool.wraptor]
# require a specific poetry version
poetry = "poetry==1.1.7"
# use the latest black
black = "black"
# install flake8 in combination with plugins
flake8 = """
flake8
flake8-bugbear
pep8-naming
flake8-isort
flake8-pytest-style"""
```

The _tool.wraptor.alias_ section can contain optional commandline aliases in the form

`alias = [tool_key:] command`

Example:
```toml
[tool.wraptor.alias]
# convenience shortcuts
run = "poetry run"
test = "poetry run pytest"

# tell pw that the isort binary is installed as part of flake8
isort = "flake8:isort"
```

Each tool gets installed in an isolated virtual environment.

These are all located in the user's platform-specific home directory under _.python-wraptor/venvs_.

This location can be modified by setting the `PYTHON_WRAPTOR_VENVS_DIR` environment variable (f.e. on your CI/CD server).

# Usage
Add `path\to\pw` in front of the usual command line.

Examples (on Windows you _may_ replace the forward slash with a backslash):
```shell
./pw poetry add -D pytest
cd src
../pw black *.py
```
pw specific options (they need to be specified immediately after `.\pw`):
```shell
# clear and re-install the virtual environment for a tool
./pw --clear poetry add requests

# upgrade a tool with pip (has no effect if the tool is specified with a fixed version in pyproject.toml)
./pw --upgrade black *.py

# display the pw version
./pw --version
```

## Why yet another tool when we already have pipx etc.?
* As Python noob I had hard times setting up a project and building existing projects
* There is always someone in the team having issues with his setup, either with a specific tool, with Homebrew, pipx, ...
* Adding tools as dev dependencies leads to dependency conflicts
* Different projects often require different versions of the same tool

## Best practices
* Separate your tools from your project dependencies
* Use a build tool with decent dependency management that locks all dependencies, 
  f.e. [Poetry](https://python-poetry.org/) and [PDM](https://pdm.fming.dev/)
* Pin down the version of your build tool to prevent the
 "I only need to change one line of code, but the project doesn't build anymore" syndrome.
 Eventually they will release a new version of the build tool with breaking changes.
* There is a category of tools that you don't want to version: tools that interact with changing environments
  like AWS. You probably want to update the AWS CLI f.e. on a regular basis by running `./pw --upgrade aws`.

## Examples
* [Facebook's PathPicker fork](https://github.com/houbie/PathPicker) with Poetry
