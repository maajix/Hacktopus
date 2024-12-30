from data_classes.flow import Flow
from data_classes.flowfile import FlowFile
from data_classes.stage import Stage
from flow.file_parser import parse_flow_file


def create_child_flow_arr(flow: Flow, _rev_list: list[list[Stage]] = None) -> list[list[Stage]]:
    """
    Recursively gather all child flows (not including the given 'flow'),
    removing any 'flow' tasks from the final data, and return them in reversed order.
    """
    if _rev_list is None:
        _rev_list = []

    # For each stage, look for tasks with execution_type == "flow"
    for stage in flow.stages:
        for task in stage.tasks:
            if task.execution_type == "flow":
                # Parse the child flow
                child_file = FlowFile(filename=f"{task.execution_data}.yaml")

                if not child_file:
                    print(f"[ERR] Could not load child-flow '{child_file.filename}'")
                    exit(-1)

                child_flow = parse_flow_file(flow_file=child_file)

                # 1) Recurse first, so we capture deeper nested flows
                create_child_flow_arr(flow=child_flow, _rev_list=_rev_list)

                # 2) Remove 'flow' tasks from the child flow’s stages
                #    (so they don't show up in the final data).
                for child_stage in child_flow.stages:
                    child_stage.tasks = [
                        t for t in child_stage.tasks if t.execution_type != "flow"
                    ]

                # 3) Now that child_flow is fully processed (its own subflows found/removed),
                #    we append it to our list of results
                _rev_list.append(child_flow.stages)

    # Return everything in reverse
    return _rev_list
