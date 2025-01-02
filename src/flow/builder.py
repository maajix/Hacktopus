from src.flow.convert_alias_to_cmd import alias_to_command
from src.data_classes.flowfile import FlowFile
from src.data_classes.stage import Stage
from src.flow.file_parser import parse_flow_file
from src.data_classes.flow import Flow
from src.flow.gather_child_flows import create_child_flow_arr
from src.utils.flow_helper import extract_variables_from
from src.execution.stage_executer import execute_flow


class FlowBuilder:
    """
    Load a flow file and modify the aliases within the tasks to contain the converted commands
    """

    def __init__(self, filename: str):
        self.flow_file_handler: FlowFile = FlowFile(filename=filename)
        self.parsed_flow_data: Flow = parse_flow_file(flow_file=self.flow_file_handler)

        # Generate an array child flow stages that will need to execute for a given child flow
        stage_list = create_child_flow_arr(flow=self.parsed_flow_data)

        # Insert the stages after the stage where the flow was called
        self._insert_child_flow_stages(stage_list=stage_list)

        # Convert all aliases to their corresponding command,
        # and change the execution_type to command
        self._replace_aliases_with_command()

    def _replace_aliases_with_command(self):
        for stage in self.parsed_flow_data.stages:
            for task in stage.tasks:
                alias_to_command(task=task)

    def _insert_child_flow_stages(self, stage_list: list[list[Stage]]):
        """
        For each sub-list of stages in stage_list, insert them into self.parsed_flow_data.stages
        in exactly the same order they appear.
        """
        for child_stages in stage_list:
            if not child_stages:
                continue  # skip an empty sub-list

            # All child_stages presumably share the same 'insert_after'
            insert_after_name = child_stages[0].insert_after
            index = self.parsed_flow_data.find_stage_index_via(stage_name=insert_after_name)
            if index is None:
                print(f"[ERR] Could not find stage '{insert_after_name}' to insert after.")
                exit(-1)

            # We'll insert each stage one after another, incrementing the position as we go.
            insert_pos = index + 1

            for child_stage in child_stages:
                self.parsed_flow_data.stages.insert(insert_pos, child_stage)
                self._append_child_vars(child_stage)
                insert_pos += 1

    def _append_child_vars(self, child_stage):
        for child_task in child_stage.tasks:
            matches = extract_variables_from(child_task.execution_data)
            for match in matches:
                self.parsed_flow_data.variables[match] = f"{{{{{match}}}}}"

    @property
    def stages(self) -> list[Stage]:
        return self.parsed_flow_data.stages

    @property
    def variables(self) -> list[str]:
        variables = []
        yaml_content = self.flow_file_handler.json
        if 'variables' in yaml_content:
            for var_name, var_value in yaml_content['variables'].items():
                if isinstance(var_value, str) and '{{' in var_value and '}}' in var_value:
                    var = var_value.strip('{{}}').strip()
                    variables.append(var)

        return list(set(variables))

    def run(self):
        from rich import print as rp
        st_out = execute_flow(stages=self.parsed_flow_data.stages)

        for key, value in st_out.items():
            rp(f"Stage: {key}")
            rp(value.decode('utf-8'))