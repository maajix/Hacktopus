from dataclasses import dataclass, field

from .stage import Stage


@dataclass(slots=True)
class Flow:
    version: str = field(default="1.0")
    name: str = field(default="")
    description: str = field(default="")
    tags: list = field(default_factory=list)
    variables: list = field(default_factory=list)
    stages: list[Stage] = field(default_factory=list)
