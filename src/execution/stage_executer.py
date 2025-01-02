import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from shlex import split
from typing import List, Optional, Dict
from rich import print as rprint

from src.data_classes.stage import Stage


def _execute_task(task, stage_name: str, stdin: Optional[bytes] = None):
    command = task.execution_data

    if task.execution_type == "flow":
        rprint(f"[FLOW] Starting flow '{task.execution_data}'")
        return ""
    elif task.execution_type == "command":
        rprint(f"[CMD:{stage_name}] Processing: {command}")
    else:
        rprint(f"[ERR] Skipping unknown execution_type '{task.execution_type}'")
        return None

    process = subprocess.Popen(
        split(command),
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE if stdin else None,
        stderr=subprocess.PIPE
    )

    if stdin:
        output, error = process.communicate(input=stdin)
    else:
        output, error = process.communicate()

    if error:
        rprint(f"[ERR:{stage_name}] {error.decode('utf-8')}")

    return output if output else None


def execute_stage_tasks(stage: Stage, stdin: Optional[bytes] = None) -> bytes:
    if not stage.parallel:
        combined_output = b''
        for task in stage.tasks:
            output = _execute_task(task, stage.name, stdin)
            if output:
                combined_output += output
        return combined_output

    outputs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(_execute_task, task, stage.name, stdin)
            for task in stage.tasks
        ]

        for future in as_completed(futures):
            try:
                if output := future.result():
                    outputs.append(output)
            except Exception as e:
                rprint(f"[ERR] Task failed: {str(e)}")

    return b''.join(outputs)


def execute_flow(stages: List[Stage]) -> dict:
    stage_outputs = {}
    stage_map = {stage.name: stage for stage in stages}

    def process_stage(stage: Stage):
        stdin = None

        # Check if any previous stage pipes to this one
        for prev_stage in stages:
            if prev_stage.pipe_output_to and stage.name in prev_stage.pipe_output_to:
                stdin = stage_outputs.get(prev_stage.name)

        output = execute_stage_tasks(stage, stdin)
        stage_outputs[stage.name] = output

        # Process next stages if this one pipes to them
        if stage.pipe_output_to and stage.pipe_output_to:
            for next_stage_name in stage.pipe_output_to:
                process_stage(stage_map[next_stage_name])

    # Start with stages that don't receive piped input
    initial_stages = [
        stage for stage in stages
        if not any(stage.name in s.pipe_output_to for s in stages if s.pipe_output_to)
    ]

    for stage in initial_stages:
        process_stage(stage)

    return stage_outputs
