from rich import print as rprint

from convert_alias_to_cmd import alias_to_command
from data_classes.flowfile import FlowFile
from file_parser import parse_flow_file
from src.data_classes.flow import Flow
from gather_child_flows import create_child_flow_arr


class FlowBuilder:
    """
    Load a flow file and modify the aliases within the tasks to contain the converted commands
    """

    def __init__(self, filename: str):
        self.flow_file_handler: FlowFile = FlowFile(filename=filename)
        self.parsed_flow_data: Flow = parse_flow_file(flow_file=self.flow_file_handler)

        # Generate filler stages for subflows
        rev_flow_list = create_child_flow_arr(flow=self.parsed_flow_data)
        rprint(rev_flow_list)
        # Convert all aliases to their corresponding command,
        # and change the execution_type to command
        self._replace_aliases_with_command()

    def _replace_aliases_with_command(self):
        for stage in self.parsed_flow_data.stages:
            for task in stage.tasks:
                alias_to_command(task=task)


builder = FlowBuilder(filename="example.yaml")
