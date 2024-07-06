"""
Simple Build Script DSL called executor with arguments, conditionals, and YAML support.

This script allows defining build tasks in a YAML file and executing them
based on dependencies and conditions.
"""
import argparse
import os
import subprocess
import sys
import yaml

from yaml import YAMLError


class Task:
    def __init__(self, name, command, arguments={}, dependencies=[], condition=None):
        self.name = name
        self.command = command
        self.arguments = arguments
        self.dependencies = dependencies
        self.condition = condition

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
        if self.condition and not eval(self.condition, context):
            print(f"Skipping task '{self.name}' due to condition.")
            return None

        # print(f" --> command: {self.command}")
        formatted_command = self.command.format(**self.arguments)
        # print(f" --> formatted_command: {formatted_command}")
        process = subprocess.Popen(formatted_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return process.returncode, output.decode(), error.decode()


def read_build_script(filename):
    """
    Reads the build script from a YAML file.

    Args:
        filename (str): The name of the YAML file containing the build script.

    Returns:
        dict: The build script dictionary parsed from the YAML file.

    Raises:
        FileNotFoundError: If the YAML file is not found.
        YAMLError: If there's an error parsing the YAML content.
    """
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Build script file '{filename}' not found.")
    except yaml.YAMLError as e:
        raise YAMLError(f"Error parsing YAML file '{filename}': {e}")


def validate_build_script(script):
    """
    Performs basic validation on the build script structure.

    Args:
        script (dict): The build script dictionary.

    Raises:
        ValueError: If any required keys are missing from a task definition.
    """
    for task_name, task_def in script.items():
        # print(f" --> task_name: {task_name}; task_def: {task_def}")
        if not all(key in task_def for key in ("command",)):
            raise ValueError(f"Task '{task_name}' in build script is missing required keys (name, command).")


def execute_build_script(script_file, context):
    """
    Executes the build script tasks based on dependencies and conditions.

    Args:
        script_file (str): The filename of the YAML file containing the build script.
        context (dict): A dictionary containing values for arguments and condition evaluation.
    """
    build_script = read_build_script(script_file)
    validate_build_script(build_script)

    completed_tasks = set()
    for task_name, task_def in build_script.items():
        # Split command into Python binary and script path
        command_parts = task_def['command'].split(" ", 1)
        script_path = os.path.join(os.path.dirname(script_file), command_parts[1])  # Modify script path
        task_def['command'] = f"{command_parts[0]} {script_path}"  # Reconstruct command

        task = Task(task_name, **task_def)  # Unpack task definition dictionary

        task.check_dependencies(completed_tasks)
        retcode, output, error = task.execute(context)

        if retcode == 0:
            print(f"Task '{task.name}' completed successfully.")
            completed_tasks.add(task.name)
        else:
            print(f"Task '{task.name}' failed with exit code {retcode}.")
            if error:
                print(f"Error output:\n{error}")
            break  # Stop execution on failure (optional)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute tasks defined in a YAML build script")
    parser.add_argument("script", help="YAML file containing the build script definition")
    parser.add_argument("-e", "--env", help="Environment variable name containing build script path (optional)")
    parser.add_argument("--no-stop", action="store_true", help="Continue execution even if a task fails")
    args = parser.parse_args()

    # Use environment variable or script argument for build script file
    script_file = args.env and os.environ.get(args.env) or args.script
    # print(f" --> script_file: {script_file}")

    context = {}  # You can add environment variables or other context values here

    execute_build_script(script_file, context)

    if not args.no_stop:
        sys.exit(None)  # Exit with the return code of the last executed task (if any)