# backend/projects.py
import json
import uuid
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Project:
    id: str
    name: str
    audio_path: str
    stems: list[str] = field(default_factory=list)

    @property
    def folder(self) -> Path:
        return Path("projects") / self.name

    @property
    def json_path(self) -> Path:
        return self.folder / "project.json"

    def save(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        data = {
            "id": self.id,
            "name": self.name,
            "audio_path": self.audio_path,
            "stems": self.stems,
        }
        with open(self.json_path, "w") as f:
            json.dump(data, f, indent=4)


class ProjectManager:
    def __init__(self):
        self.projects: dict[str, Project] = {}
        self.load_all_projects()

    # -----------------------------
    # Create new project
    # -----------------------------
    def create_project(self, audio_path: str, name: str) -> Project:
        project_id = str(uuid.uuid4())
        project = Project(id=project_id, name=name, audio_path=audio_path)
        self.projects[project_id] = project
        project.save()
        return project

    # -----------------------------
    # Add stems + save
    # -----------------------------
    def add_stems(self, project_id: str, stems: list[str]):
        if project_id in self.projects:
            project = self.projects[project_id]
            project.stems = stems
            project.save()

    # -----------------------------
    # Load all project.json files
    # -----------------------------
    def load_all_projects(self):
        root = Path("projects")
        if not root.exists():
            return

        for folder in root.iterdir():
            json_file = folder / "project.json"
            if json_file.exists():
                with open(json_file, "r") as f:
                    data = json.load(f)

                project = Project(
                    id=data["id"],
                    name=data["name"],
                    audio_path=data["audio_path"],
                    stems=data.get("stems", []),
                )
                self.projects[project.id] = project

    # -----------------------------
    # List all projects
    # -----------------------------
    def list_projects(self) -> list[Project]:
        return list(self.projects.values())


# Global shared instance
project_manager = ProjectManager()