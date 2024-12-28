from src.data_classes.file_handler import flow_file_handler
from src.data_classes.flow_data_handler import flow_data


def yaml_to_json(filename: str) -> flow_data:
    file_handler = flow_file_handler(filename=filename)
    data_handler = flow_data(file_handler=file_handler)
    return data_handler
