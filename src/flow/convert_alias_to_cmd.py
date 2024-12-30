from __future__ import annotations

import os.path
from pathlib import Path

import yaml

from src.data_classes.task import Task


def _find_tool_path_via(name: str) -> dict | False:
    root_folder = Path(__file__).parent.parent.parent.absolute()
    tool_folder = Path(root_folder, "tools", name)

    if os.path.exists(tool_folder):
        return tool_folder
    else:
        return False


def alias_to_command(task: Task) -> Task | None:
    if task.execution_type == 'alias':
        tool_name, alias = task.execution_data.split(":")
        tool_folder = _find_tool_path_via(tool_name)

        if tool_folder:
            aliases_file = Path(tool_folder, "aliases.yaml")
            config_file = Path(tool_folder, "config.yaml")

            with open(aliases_file, 'r') as f:
                alias_command = yaml.safe_load(f).get("aliases").get(alias).get("command")

            with open(config_file, 'r') as f:
                run_command = yaml.safe_load(f).get("run_command")

            if run_command and alias_command:
                task.execution_type = "command"
                task.execution_data = f"{run_command} {alias_command}"
            else:
                print(f"[ERR] Could not convert alias to command for '{task.execution_data}'")

        else:
            print(f"[ERR] Could not find tool folder for '{task.execution_data}'")
            exit(-1)

        return task
    else:
        return None