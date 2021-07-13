# Python wraptor

__Alpha quality (requires additional testing on *nix and Windows support needs to be finished)__

CLI wrapper for automatic installation of Python tools:
* Make it be a breeze for others to get started with your project
* Get reproducible builds by always using the correct versions of your build tools

![velociraptor](docs/velociraptor.png)

## Installation
Copy _pw_ and _pw.bat_ to your project's root folder and add it in version control.

Having _python3_ and _pip3_ (>= 3.6) available on your path is the only prerequisite.

## Configuration
Add the _tool.wraptor_ section inside _pyproject.toml_ in your project's root folder.
Each entry has the form `tool = "pip install arguments"`

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

The _tool.wraptor.alias_ section can contain optional commandline aliases in the form `alias = [tool_key:] command`

Example:
```toml
[tool.wraptor.alias]
# convenient shortcuts
run = "poetry run"
test = "poetry run pytest"

# isort is installed as part of flake8 in the tool.wraptor section
isort = "flake8:isort"
```

Each tool gets installed in an isolated virtual environment.

These are all located in the user's platform-specific home directory under _.python-wraptor/venvs_.

This can be modified by setting the `PYTHON_WRAPTOR_DIR` environment variable (f.e. on your CI/CD server).

# Usage
Add `path\to\pw` in front of the usual command line.

Examples:
```shell
./pw poetry add -D pytest
cd src
../pw black *.py
```

**TODO** Windows support


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
 Eventually your build tool wil get breaking changes.
