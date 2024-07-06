"""
Simple Script DSL called executor with arguments, conditionals, and YAML support.

This script allows defining tasks in a YAML file and executing them
based on dependencies and conditions.
"""
import argparse
import ast
# import compile
import datetime
import os
import subprocess
import sys
import yaml

from yaml import YAMLError


class Task:
    def __init__(self, name, command, arguments={}, dependencies=[], enabled=True):
        self.name = name
        self.command = command
        self.arguments = arguments
        self.dependencies = dependencies
        self.enabled = enabled

    def check_dependencies(self, completed_tasks):
        """
        Checks if all dependencies of the task are completed.

        Args:
            completed_tasks (set): A set containing names of completed tasks.

        Raises:
            RuntimeError: If any dependency is not found in completed_tasks.
        """
        for dependency in self.dependencies:
            if dependency not in completed_tasks:
                raise RuntimeError(f"Task '{self.name}' depends on incomplete task '{dependency}'")

    def execute(self, context):
        """
        Executes the task's command with arguments and context.

        Args:
            context (dict): A dictionary containing values for arguments and condition evaluation.

        Returns:
            tuple: A tuple containing the process return code, standard output, and standard error (if any).
        """
        print(f"self.enabled = {self.enabled}")
        # if self.enabled and not eval(self.enabled, context):
        if not self.enabled:
            print(f"Task '{self.name}' skipped since it is disabled.")
            retcode = -1    # return code defined for skipped task
            output = None
            error = ""
            return retcode, output, error

        # print(f" --> command: {self.command}")
        formatted_command = self.command.format(**self.arguments)
        # print(f" --> formatted_command: {formatted_command}")
        with open(f"executor_log.txt", "a") as log_file:  # Open log file in append mode
            process = subprocess.Popen(formatted_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"\n** Task: {self.name} ({timestamp}) **\n")
            log_file.write(f"Command: {formatted_command}\n")
            log_file.write(f"Standard Output:\n")
            prefix = "   "
            for line in output.decode().splitlines():
                log_file.write(f"{prefix}{line}\n")
            if error:
                log_file.write(f"Standard Error:\n")
                for line in error.decode().splitlines():
                    log_file.write(f"{prefix}{line}\n")
            log_file.write("\n")
            log_file.write(50*"-")
            log_file.write("\n")
        return process.returncode, output.decode(), error.decode()


def read_script(filename):
    """
    Reads the script from a YAML file.

    Args:
        filename (str): The name of the YAML file containing the script.

    Returns:
        dict: The script dictionary parsed from the YAML file.

    Raises:
        FileNotFoundError: If the YAML file is not found.
        YAMLError: If there's an error parsing the YAML content.
    """
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Script file '{filename}' not found.")
    except yaml.YAMLError as e:
        raise YAMLError(f"Error parsing YAML file '{filename}': {e}")


def validate_script(script):
    """
    Performs basic validation on the script structure.

    Args:
        script (dict): The script dictionary.

    Raises:
        ValueError: If any required keys are missing from a task definition.
    """
    for task_name, task_def in script.items():
        # print(f" --> task_name: {task_name}; task_def: {task_def}")
        if not all(key in task_def for key in ("command",)):
            raise ValueError(f"Task '{task_name}' in script is missing required keys (command).")


def execute_script(script_file, context):
    """
    Executes the script tasks based on dependencies and conditions.

    Args:
        script_file (str): The filename of the YAML file containing the script.
        context (dict): A dictionary containing values for arguments and condition evaluation.
    """
    build_script = read_script(script_file)
    validate_script(build_script)

    completed_tasks = set()
    for task_name, task_def in build_script.items():
        # Split command into Python binary and script path
        command_parts = task_def['command'].split(" ", 1)
        script_path = os.path.join(os.path.dirname(script_file), command_parts[1])  # Modify script path
        task_def['command'] = f"{command_parts[0]} {script_path}"  # Reconstruct command

        task = Task(task_name, **task_def)  # Unpack task definition dictionary

        task.check_dependencies(completed_tasks)
        retcode, output, error = task.execute(context)

        if retcode == -1:
            continue
        elif retcode == 0:
            print(f"Task '{task.name}' completed successfully.")
            completed_tasks.add(task.name)
        else:
            print(f"Task '{task.name}' failed with exit code {retcode}.")
            if error:
                print(f"Error output:\n{error}")
            break  # Stop execution on failure (optional)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute tasks defined in a YAML script")
    parser.add_argument("script", help="YAML file containing the script definition")
    parser.add_argument("-e", "--env", help="Environment variable name containing script path (optional)")
    parser.add_argument("--no-stop", action="store_true", help="Continue execution even if a task fails")
    args = parser.parse_args()

    # Use environment variable or script argument for build script file
    script_file = args.env and os.environ.get(args.env) or args.script
    # print(f" --> script_file: {script_file}")

    # TODO: Implement the context feature
    context = {}  # Add environment variables or other context values here

    # TODO: When a task is disabled and it is a dependency of another one
    #       this task fails with a RuntimeError:
    #       self.enabled = True
    #       Task 'hello' completed successfully.
    #       self.enabled = False
    #       Task 'bye' skipped since it is disabled.
    #       Traceback (most recent call last):
    #         File "/home/dmaldona/projects/executor/executor.py", line 171, in <module>
    #           execute_script(script_file, context)
    #         File "/home/dmaldona/projects/executor/executor.py", line 142, in execute_script
    #           task.check_dependencies(completed_tasks)
    #         File "/home/dmaldona/projects/executor/executor.py", line 39, in check_dependencies
    #           raise RuntimeError(f"Task '{self.name}' depends on incomplete task '{dependency}'")
    #       RuntimeError: Task 'hello2' depends on incomplete task 'bye'
    execute_script(script_file, context)

    # TODO: Implement the no_stop feature
    if not args.no_stop:
        sys.exit(None)