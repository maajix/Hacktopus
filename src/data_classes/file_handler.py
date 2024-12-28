import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class flow_file_handler:
    filename: str
    extension: str = field(default="yaml")
    is_flow_file_existing: bool = field(default=False)
    flow_file_full_path: Path = field(default_factory=Path)
    root_dir: Path = Path(__file__).parent.parent.parent.absolute()
    flow_root_dir: Path = Path(root_dir, "flows")

    def __post_init__(self):
        self.extension = self.filename.split(".")[-1]
        self.flow_file_full_path = Path(self.flow_root_dir, f"{self.filename}")
        print(self.flow_file_full_path)
        if os.path.exists(self.flow_file_full_path):
            self.is_flow_file_existing = True
