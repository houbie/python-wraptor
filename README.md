# Python wraptor

CLI wrapper for automatic installation of Python tools:
* Make it be a breeze for others to get started with your project or tutorial
* Get reproducible builds by always using the correct versions of your build tools
* Plays well with build tools like [Poetry](https://python-poetry.org/)

![velociraptor](docs/velociraptor.png)

## Installation
No tools to install (besides Python 3) 😍

![Cast](./docs/poetry-build-cast.svg)

Copy _pw_ and _pw.bat_ to your project's root directory and add it under version control.

_python3_ (or _python_ on Windows) >= 3.6 and _pip3_ must be available on your path.

## Configuration
Add the _tool.wraptor_ section inside _pyproject.toml_ in your project's root directory.

Each entry has the form

`tool = "pip-install-arguments"`

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

# simple shell commands
clean = "rm -f .coverage && rm -rf .pytest_cache"

# when combining multiple wraptor aliases, prefix them with ./pw
check-pylint = "./pw poetry run pylint && ./pw tests"

# push to git if all checks pass
release = "&: check push"
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

_pw_ specific options:
```shell
# upgrade a tool with pip (has no effect if the tool is specified with a fixed version in pyproject.toml)
./pw --pw-upgrade black

# clear and re-install the virtual environment for a tool
./pw --pw-clear poetry

# clear the complete wraptor cache
./pw --pw-clear-all poetry
```

## Bonus
If you want to avoid typing `./pw` (or `../pw` when in a subdirectory), you can copy the _px_ script to a
location on your PATH (f.e. _/usr/local/bin_, or create a symlink with `ln -fs $(pwd)/px /usr/local/bin/px`).

From then on, you can replace _pw_ with _px_ and invoke it from any (sub)directory containing the _pw_ script.
```shell
cd my-pw-project
px test
cd tests
px test sometest.py
```

## Uninstall / cleaning up
To clean up everything that was installed via the Python Wraptor, just delete the _.python-wraptor_ directory
in your home directory or run `./pw --pw-clear-all`

## Why yet another tool when we already have pipx etc.?
* As Python noob I had hard times setting up a project and building existing projects
* There is always someone in the team having issues with his setup, either with a specific tool, with Homebrew, pipx, ...
* Adding tools as dev dependencies leads to dependency conflicts
* Different projects often require different versions of the same tool

## Best practices
* Separate your tools from your project dependencies
* Use a build tool with decent dependency management that locks all dependencies,
  f.e. [Poetry](https://python-poetry.org/) or [PDM](https://pdm.fming.dev/)
* Pin down the version of your build tool to prevent the "project doesn't build anymore" syndrome.
 Eventually a new version of the build tool with breaking changes will be released.
* There is a category of tools that you don't want to version: tools that interact with changing environments.
  You probably want to update those on a regular basis by running `./pw --upgrade my-evolving-tool`.

## Examples
* This project (using Poetry)
* [Wraptor examples](https://github.com/houbie/wrapped-pi)
* [Facebook's PathPicker fork](https://github.com/houbie/PathPicker) (using Poetry)

## TODO
* allow quoted strings in command arguments
* display available tools and aliases as part of the help message
* px script for Windows
* init script that copies the pw scripts and initializes pyproject.toml + publish to PyPi
