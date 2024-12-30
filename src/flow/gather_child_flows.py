from data_classes.flow import Flow
from data_classes.flowfile import FlowFile
from data_classes.stage import Stage
from flow.file_parser import parse_flow_file


def create_child_flow_arr(
        flow: Flow,
        _rev_list: list[list[Stage]] = None,
        _insert_after: str = None
) -> list[list[Stage]]:
    """
    Recursively gather all child flows (not including the given 'flow'),
    removing any 'flow' tasks from the final data, and return them in
    reversed order (relative to discovery) for the *stages themselves*.

    Tasks within each stage remain in their original order as returned
    by parse_flow_file (i.e., we do NOT reverse tasks).
    """
    try:
        if _rev_list is None:
            _rev_list = []

        for stage in flow.stages:
            for task in stage.tasks:
                if task.execution_type == "flow":
                    if _insert_after is None and stage.name:
                        _insert_after = stage.name

                    # Load the child flow from <execution_data>.yaml
                    child_file = FlowFile(filename=f"{task.execution_data}.yaml")
                    child_flow = parse_flow_file(flow_file=child_file)

                    # Recurse for sub-child flows
                    create_child_flow_arr(
                        flow=child_flow,
                        _rev_list=_rev_list,
                        _insert_after=_insert_after
                    )

                    # Remove any 'flow' tasks in the child's stages
                    for child_stage in child_flow.stages:
                        child_stage.tasks = [
                            t for t in child_stage.tasks
                            if t.execution_type != "flow"
                        ]

                    # Update insert_after
                    for child_stage in child_flow.stages:
                        child_stage.insert_after = _insert_after
                        child_stage.name = "_internal_child_flow"

                    # Insert these child stages *at the front*
                    _rev_list.insert(0, child_flow.stages)

        # Return the final list as-is (no additional slicing)
        return _rev_list

    except RecursionError:
        print("[ERR] Recursive flow calling detected, please check YAML files")
        exit(-1)
