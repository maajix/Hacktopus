import re
from src.data_classes.stage import Stage


def extract_variables_from(value: str) -> list[str]:
    """
    Extracts all variables enclosed within curly braces ({{}}) from a given string and returns them as a list.
    :param value: the input string from which variables are to be extracted
    :return: list of extracted variable strings

    :Example:
    >>> extract_variables_from("{{name}} is {{age}} years old")
    """
    pattern = r'(\{\{[^}]+\}\})'
    if isinstance(value, str):
        matches = re.findall(pattern, value)
        return [match.replace("{{", "").replace("}}", "") for match in matches]


def replace_exec_data_vars(final_vars: dict, stages: list[Stage]) -> None:
    """
    This function takes a list of stages and replaces any variables in their task execution data
    with the corresponding values from the final_vars dictionary.
    :param stages: list of Stage objects
    :param final_vars: dictionary containing the variables

    :Example:
    >>> replace_exec_data_vars({"url": "{{url}}"}, example_stage)
    """
    for stage in stages:
        for task in stage.tasks:
            matches = extract_variables_from(task.execution_data)
            for match in matches:
                if match in final_vars:
                    task.execution_data = task.execution_data.replace(f"{{{{{match}}}}}", final_vars.get(match))
