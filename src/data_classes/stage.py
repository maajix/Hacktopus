from dataclasses import dataclass, field
from .task import Task


@dataclass(slots=True)
class Stage:
    name: str = field(default="")
    description: str = field(default="")
    parallel: bool = field(default=False)
    insert_after: str = field(default=None)
    pipe_output_to: str = field(default="")
    tasks: list[Task] = field(default_factory=list)
