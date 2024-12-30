from __future__ import annotations

from dataclasses import dataclass, field

from .stage import Stage


@dataclass(slots=True)
class Flow:
    version: str = field(default="1.0")
    name: str = field(default="")
    description: str = field(default="")
    tags: list = field(default_factory=list)
    variables: dict = field(default_factory=dict)
    stages: list[Stage] = field(default_factory=list)

    def find_stage_index_via(self, stage_name) -> int | None:
        for i, stage in enumerate(self.stages):
            if stage.name == stage_name:
                return i
        return None
