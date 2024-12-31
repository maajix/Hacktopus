from src.flow.builder import FlowBuilder
from src.data_classes.task import Task
from src.data_classes.stage import Stage
from src.execution.stage_executer import execute_stage_tasks

from rich import print as rprint

example_stage = Stage()
example_stage.name = "test"

task_ls = Task()
task_ls.execution_data = "ls -la"

task_echo = Task()
task_echo.execution_data = 'echo "Hello World!"'

example_stage.tasks.append(task_ls)
example_stage.tasks.append(task_echo)

# execute_stage_tasks(example_stage, stream_live_output=True)

builder = FlowBuilder(filename="example.yaml")
for stage in builder.parsed_flow_data.stages:
    rprint(stage)
