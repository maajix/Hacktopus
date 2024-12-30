import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(slots=True)
class FlowFile:
    filename: str
    extension: str = field(default="yaml")
    is_file_existing: bool = field(default=False)
    full_path: Path = field(default_factory=Path)
    project_root_dir: Path = Path(__file__).parent.parent.parent.absolute()
    flow_root_dir: Path = Path(project_root_dir, "flows")
    json: dict = field(default_factory=dict)

    def __post_init__(self):
        self.extension = self.filename.split(".")[-1]
        self.full_path = Path(self.flow_root_dir, f"{self.filename}")

        if os.path.exists(self.full_path):
            self.is_file_existing = True

        if self.is_file_existing:
            with open(self.full_path, 'r') as f:
                self.json = yaml.safe_load(f)
        else:
            print(f"[ERR] Flow file '{self.full_path}' could not be found")
            exit(-1)

