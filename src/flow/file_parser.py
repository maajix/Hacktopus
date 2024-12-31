from src.data_classes.flowfile import FlowFile
from src.data_classes.flow import Flow
from src.data_classes.stage import Stage
from src.data_classes.task import Task


def parse_flow_file(flow_file: FlowFile) -> Flow:
    from rich.console import Console
    console = Console()
    flow = Flow()
    json_data = flow_file.json if flow_file.json else {}

    def _check_missing(keys: list) -> None:
        for key_to_check in keys:
            if key_to_check not in json_data.keys():
                console.print(f"[ERR] Missing '{key_to_check}' key in '{flow_file.filename}'")
                exit(-1)

    try:
        flow.version = json_data.get("version")
        flow.name = json_data.get("name")
        flow.description = json_data.get("description")
        flow.tags = json_data.get("tags")
        flow.variables = json_data.get("variables")
        flow.stages = []

        required_keys = ["name", "description", "variables", "container"]
        _check_missing(required_keys)

        container = json_data.get("container")
        tmp_stage = Stage()
        for stage in container:
            stage_data = container.get(stage)

            tmp_stage.name = stage
            tmp_stage.parallel = stage_data.get("parallel")
            tmp_stage.description = stage_data.get("description")
            tmp_stage.tasks = []
            try:
                tmp_task = Task()
                for task in stage_data.get("tasks"):
                    if "alias" in task.keys():
                        tmp_task.execution_type = "alias"
                    elif "command" in task.keys():
                        tmp_task.execution_type = "command"
                    elif "flow" in task.keys():
                        tmp_task.execution_type = "flow"
                    else:
                        print(f"[WRN] Unknown execution type in '{tmp_stage.name}', skipping stage")

                    if tmp_task.execution_type:
                        tmp_task.execution_data = task.get(tmp_task.execution_type)

                    if "options" in task.keys():
                        tmp_task.execution_options = task.get("options")

                    tmp_stage.tasks.append(tmp_task)
                    tmp_task = Task()
            except KeyError as e:
                pass

            flow.stages.append(tmp_stage)
            tmp_stage = Stage()

    except KeyError:
        console.print(f"[ERR] Could not parse json data")
        console.print(json_data)
    return flow
