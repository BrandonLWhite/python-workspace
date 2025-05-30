# python-workspace
python-workspace is a command line interface (CLI) tool `pyworks` for helping you run developer commands against multiple Python projects residing in subdirectories of a "workspace" directory.

Python projects are dynamically discovered by recursively finding pyproject.toml files in the directory structure, honoring any `.gitignore` patterns.

Currently the package manager commands are Poetry-specific, but support for more package managers in the future is a goal.

## Installation
Install using [pipx](https://github.com/pypa/pipx)
```
pipx install python-workspace
```

This will install the `pyworks` command.

## Usage
All operations are performed using the `pyworks` CLI script.
Example:
```
pyworks install
```
If run the from the root directoy of a multi-project Python repository, this command would invoke `poetry install` on each sub-project using parallel processes.

## Commands
### install
Run `poetry install` on all projects.

### sync
Run `poetry sync` on all projects.

### lock
Run `poetry lock` on all projects.

### recreate
Recreate all virtual environments by running the following sequence on all projects:
```
poetry env remove --all
poetry install
```

### remove
Run `poetry env remove --all` on all projects

### exec
Execute an arbitrary command that you specify on all projects.

Example:
This command would execute `ls -l` within each project's directory.
```
pyworks exec ls -l
```

### list
Output a listing of all projects found, by project name and path to the pyproject.toml file.

### test
Run the `test` project task on all projects.

### package
Run the `package` project task on all projects.

## Project tasks
For developer task scripts defined in the pyproject.toml file (e.g. `test` and `package`) the following well-known pyproject.toml key
paths are checked in the order shown and the first one encountered with a value is used for the shell command.

1. `tool.tasks`
2. `tool.pdm.scripts`
3. `tool.poe.tasks`
