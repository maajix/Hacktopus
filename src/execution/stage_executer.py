import subprocess
import threading
from shlex import split

from src.data_classes.task import Task
from src.data_classes.stage import Stage


def _execute(task: Task, stream_live_output=False) -> str:
    command = task.execution_data

    if not stream_live_output:
        process = subprocess.Popen(split(command), stdout=subprocess.PIPE)

        # Ensure the process finishes
        output, error = process.communicate()
        return output.decode('utf-8') if output else None
    else:
        output = []

        def stream_output():
            process = subprocess.Popen(split(command), stdout=subprocess.PIPE)

            for line in iter(process.stdout.readline, b''):
                print(line.decode('utf-8').strip())
                output.append(line.decode('utf-8'))

            # Ensure the process finishes
            process.wait()

    # Start a separate thread to handle output streaming
    output_thread = threading.Thread(target=stream_output)
    output_thread.start()

    # Wait for the output thread to complete
    output_thread.join()

    # Return the final stdout
    return "".join(output)


def execute_stage_tasks(stage: Stage, stream_live_output: bool = False) -> str:
    combined_output = []
    for task in stage.tasks:
        combined_output.append(_execute(task, stream_live_output=stream_live_output))
    return "".join(combined_output)
