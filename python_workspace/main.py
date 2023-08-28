"""
TODO:
- Reusable parallel process loop
- CLI parser
- install command (async)
- test command (async)
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
    argparser.add_argument('operation', choices=['install', 'test', 'list', 'lock', 'recreate', 'remove'])
    argparser.add_argument('--path')
    argparser.add_argument('pass-through', nargs=argparse.REMAINDER)
    args = argparser.parse_args()

    workspace_root = Path.cwd()
    workspace = Workspace(workspace_root)

    asyncio.run(run_operation(args.operation, workspace))


async def run_operation(operation: str, workspace: Workspace):
    if operation == 'install':
        await install_projects(workspace)
    elif operation == 'test':
        await test_projects(workspace)
    elif operation == 'lock':
        await run_project_command_parallel(workspace.poetry_projects, f"{POETRY_BASE_COMMAND} lock --no-update")
    elif operation == 'remove':
        await run_project_command_parallel(workspace.poetry_projects, f"{POETRY_BASE_COMMAND} env remove --all")
    elif operation == 'recreate':
        # TODO
        pass


async def run_project_command_parallel(projects: list[Project], command: str):
    tasks = []
    for project in projects:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=project.root_path)
        tasks.append(tail_output_async(process.stdout, project.name))
        tasks.append(tail_output_async(process.stderr, project.name))
        tasks.append(process.wait())

    await asyncio.gather(*tasks)


async def tail_output_async(stream, label: str):
    async for line in stream:
        print(f"{label}: {line.decode().strip()}")


async def install_projects(workspace: Workspace):
    await run_project_command_parallel(workspace.poetry_projects, f"{POETRY_BASE_COMMAND} install")


async def test_projects(workspace: Workspace):
    # TODO -- Add way for the Project to specify what command to run for the test.
    await run_project_command_parallel(workspace.poetry_projects, f"{POETRY_BASE_COMMAND} run pytest --color=yes")
