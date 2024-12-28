from dataclasses import dataclass, field
from .task import Task


@dataclass(slots=True)
class Stage:
    name: str = field(default="")
    parallel: bool = field(default=False)
    description: str = field(default="")
    tasks: list[Task] = field(default_factory=list)
    started: bool = field(default=False)
    done: bool = field(default=False)
