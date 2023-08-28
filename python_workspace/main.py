"""
TODO:
- CLI parser
- list command
"""
import argparse
import asyncio
from pathlib import Path

from .workspace import Workspace
from .project import Project

POETRY_BASE_COMMAND = "poetry --ansi"

def main():
    argparser = argparse.ArgumentParser(description='TODO Description')
    argparser.add_argument('operation', choices=['install', 'test', 'list', 'lock', 'recreate', 'remove', 'exec'])
    argparser.add_argument('--path')
    argparser.add_argument('passthrough', nargs=argparse.REMAINDER)
    args = argparser.parse_args()

    workspace_root = Path.cwd()
    workspace = Workspace(workspace_root)

    asyncio.run(run_operation(args.operation, args.passthrough, workspace))


async def run_operation(operation: str, passthrough_args: list[str], workspace: Workspace):
    if operation == 'install':
        await install_projects(workspace)
    elif operation == 'test':
        await test_projects(workspace)
    elif operation == 'lock':
        await workspace.run_project_command_parallel(f"{POETRY_BASE_COMMAND} lock --no-update")
    elif operation == 'remove':
        await remove_all_venvs(workspace)
    elif operation == 'recreate':
        await recreate_all_venvs(workspace)
    elif operation == 'exec':
        await workspace.run_project_command_parallel(" ".join(passthrough_args))


async def install_projects(workspace: Workspace):
    await workspace.run_project_command_parallel(f"{POETRY_BASE_COMMAND} install")


async def recreate_all_venvs(workspace: Workspace):
    await remove_all_venvs(workspace)
    await install_projects(workspace)


async def remove_all_venvs(workspace: Workspace):
    await workspace.run_project_command_parallel(f"{POETRY_BASE_COMMAND} env remove --all")


async def test_projects(workspace: Workspace):
    # TODO -- Add way for the Project to specify what command to run for the test.
    await workspace.run_project_command_parallel(f"{POETRY_BASE_COMMAND} run pytest --color=yes")
