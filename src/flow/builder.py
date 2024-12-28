from data_classes.flowfile import FlowFile
from file_parser import parse_flow_file
from icecream import ic
from src.data_classes.flow import Flow


class FlowBuilder:
    def __init__(self, filename: str):
        self.flow_file: FlowFile = FlowFile(flow_filename=filename)
        self.parsed_flow: Flow = parse_flow_file(flow_file=self.flow_file)
