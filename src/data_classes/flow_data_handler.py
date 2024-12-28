from dataclasses import dataclass, field
from .file_handler import flow_file_handler
import yaml


@dataclass(slots=True)
class flow_data:
    file_handler: flow_file_handler
    json: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.file_handler.is_flow_file_existing:
            with open(self.file_handler.flow_file_full_path, 'r') as f:
                data = yaml.safe_load(f)
                self.json = data if data else {}
        else:
            raise FileNotFoundError(
                f"Flow file '{self.file_handler.flow_file_full_path}' could not be found")
