from pathlib import Path
from dataclasses import dataclass
from functools import cached_property
from typing import Optional
import tomli


@dataclass
class Project:
    pyproject_path: Path

    @cached_property
    def toml(self) -> dict:
        return tomli.loads(self.pyproject_path.read_text())

    @property
    def root_path(self) -> Path:
        return self.pyproject_path.parent

    @property
    def name(self) -> str:
        return self.poetry_config.get('name', 'NoName')

    @property
    def poetry_config(self) -> Optional[dict]:
        return self.toml.get('tool', {}).get('poetry', {})

    @property
    def is_poetry_project(self) -> bool:
        return bool(self.poetry_config)
