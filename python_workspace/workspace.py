import subprocess
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from .project import Project

@dataclass
class Workspace:
    root_path: Path

    @cached_property
    def projects(self) -> list[Project]:
        ls_files_result = subprocess.run(f"git ls-files {self.root_path}", shell=True, capture_output=True, text=True)
        all_files = ls_files_result.stdout.split('\n')
        all_file_paths = (Path(file) for file in all_files)

        return [
            Project(path) for path in all_file_paths if path.name == 'pyproject.toml'
        ]

    @cached_property
    def poetry_projects(self) -> list[Project]:
        return [
            project for project in self.projects if project.is_poetry_project
        ]
