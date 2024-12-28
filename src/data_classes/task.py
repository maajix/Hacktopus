from dataclasses import dataclass, field


@dataclass(slots=True)
class Task:
    execution_type: str = field(default="")
    execution_data: str = field(default="")
    execution_options: list = field(default_factory=list)
