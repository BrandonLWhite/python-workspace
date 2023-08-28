import asyncio

from .project import Project


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
