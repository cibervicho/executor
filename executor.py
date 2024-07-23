"""
Simple Script DSL called executor with arguments, conditionals, and YAML support.

This script allows defining tasks in a YAML file and executing them
based on dependencies and conditions.
"""
import argparse
import datetime
import os
import subprocess
import yaml

from collections import namedtuple
from sys import exit
from yaml import YAMLError


class Task:
    def __init__(self, name, command, arguments={}, dependencies=[], enabled=True, test_dir=""):
        """
        Initializes a Task object.

        Args:
            name (str): The name of the task.
            command (str): The command to be executed.
            arguments (dict, optional): A dictionary containing arguments for the command. Defaults to {}.
            dependencies (list, optional): A list of task names that this task depends on. Defaults to [].
            enabled (bool, optional): A boolean value indicating whether the task is enabled. Defaults to True.
        """
        self.name = name
        self.command = command
        self.arguments = arguments
        self.dependencies = dependencies
        self.enabled = enabled
        self.test_dir = test_dir

    def check_dependencies(self, completed_tasks, tasks):
        """
        Checks if all dependencies of the task are completed and enabled.

        Args:
            completed_tasks (set): A set containing names of completed and enabled tasks.

        Returns:
            bool: A boolean value indicating whether the task can be executed based on its dependencies.

        Note:
            This method assumes that the 'tasks' dictionary contains all tasks defined in the script,
            with their names as keys and Task objects as values.
        """
        can_run = True
        for dependency in self.dependencies:
            if dependency not in completed_tasks or not tasks[dependency].enabled:
                error_msg = f"Task '{self.name}' depends on incomplete task '{dependency}'"
                print(error_msg)
                can_run = False

        return can_run

    def execute(self, context):
        """
        Executes the task's command with arguments and context.

        Args:
            context (dict): A dictionary containing values for arguments and condition evaluation.

        Returns:
            tuple: A tuple containing the process return code, standard output, and standard error (if any).
        """
        if not self.enabled:
            print(f"Task '{self.name}' skipped since it is disabled.")
            retcode = -1    # return code defined for skipped task
            output = None
            error = ""
            return retcode, output, error

        saved_dir = os.getcwd()
        os.chdir(self.test_dir)

        formatted_command = self.command.format(**self.arguments)
        print(f"Task '{self.name}' command: {formatted_command}")
        with open(f"{saved_dir}/log/executor_log.txt", "a") as log_file:  # Open log file in append mode
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

        os.chdir(saved_dir)
        return process.returncode, output.decode(), error.decode()

    def __str__(self):
        return f"Task Name: {self.name}\n \
                Command: {self.command}\n \
                Arguments: {self.arguments}\n \
                Dependencies: {self.dependencies}\n \
                Enabled: {self.enabled}\n \
                Test Directory: {self.test_dir}"


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

    This function reads a script from a YAML file and returns the parsed script dictionary.
    If the YAML file is not found, it raises a FileNotFoundError. If there's an error parsing
    the YAML content, it raises a YAMLError.
    """
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Script file '{filename}' not found.")
        #exit(1)
        raise FileNotFoundError(f"Error: Script file '{filename}' not found.")

    except yaml.YAMLError as e:
        print(f"Error: Error parsing YAML file '{filename}': {e}")
        #exit(1)
        raise YAMLError(f"Error: Error parsing YAML file '{filename}': {e}")


def validate_script(script):
    """
    Validates the structure of the script dictionary.

    Args:
        script (dict): The script dictionary parsed from YAML.

    Raises:
        ValueError: If a task definition is missing a required key (command).
        ValueError: If an optional key has an invalid data type.
    """

    TaskDef = namedtuple("TaskDef", ["command", "enabled", "arguments", "dependencies"])

    # Validate each task definition
    for task_name, task_def in script.items():
        # Convert task definition to namedtuple for type checking
        task_def = TaskDef(command=task_def.get("command"), enabled=task_def.get("enabled", True), arguments=task_def.get("arguments", None), dependencies=task_def.get("dependencies", None))

        # Check for required key
        if not task_def.command:
            raise ValueError(f"Task '{task_name}' is missing required key 'command'.")

        # Check optional keys if present
        if task_def.enabled is not None and not isinstance(task_def.enabled, bool):
            raise ValueError(f"Task '{task_name}' has invalid data type for 'enabled' (expected bool).")

        if task_def.arguments is not None and not isinstance(task_def.arguments, dict):
            raise ValueError(f"Task '{task_name}' has invalid data type for 'arguments' (expected dict).")

        if task_def.dependencies is not None and not isinstance(task_def.dependencies, list):
            raise ValueError(f"Task '{task_name}' has invalid data type for 'dependencies' (expected list).")

        # Add further validation for arguments and dependencies structure if needed here.

    print(f"Script '{script_file}' structure is valid.")


def get_all_tasks(build_script):
    """
    Extracts all tasks from the provided script dictionary and returns a dictionary where
    task names are keys and Task objects are values.

    Args:
        build_script (dict): The script dictionary parsed from a YAML file.

    Returns:
        dict: A dictionary containing task names as keys and Task objects as values.
    """
    tasks = {}
    for task_name, task_def in build_script.items():
        task = Task(task_name, **task_def)
        tasks[task_name] = task
    return tasks


def execute_script(script_file, context):
    """
    Executes the script tasks based on dependencies and conditions.

    Args:
        script_file (str): The filename of the YAML file containing the script.
        context (dict): A dictionary containing values for arguments and condition evaluation.

    Returns:
        None: This function does not return any value. It prints the status of each task execution.

    Raises:
        FileNotFoundError: If the YAML file is not found.
        YAMLError: If there's an error parsing the YAML content.
    """
    build_script = read_script(script_file)
    validate_script(build_script)

    tasks = get_all_tasks(build_script)

    completed_tasks = set()
    current_dir = os.path.dirname(script_file)
    for task_name, task_def in build_script.items():
        task_def['test_dir'] = os.path.join(os.getcwd(), current_dir)

        task = Task(task_name, **task_def)

        if can_run := task.check_dependencies(completed_tasks, tasks):
            retcode, output, error = task.execute(context)

            if retcode == -1:  # Task skipped
                continue
            elif retcode == 0:
                print(f"Task '{task.name}' completed successfully.")
                completed_tasks.add(task.name)
            else:
                print(f"Task '{task.name}' failed with exit code {retcode}.")
                if error:
                    print(f"Error output:\n{error}")
                if not context.get("no_stop"):
                    break  # Stop execution on failure (optional)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute tasks defined in a YAML script")
    parser.add_argument("script", nargs="?", help="YAML file containing the script definition.")
    parser.add_argument("--no-stop", action="store_true", help="Continue execution even if a task fails.")
    args = parser.parse_args()

    # If script argument is not provided, check for environment variable
    if not args.script:
        script_path = os.environ.get("EXECUTOR_SCRIPT_PATH")
        if script_path:
            args.script = script_path
        else:
            print("Error: Script path not provided and environment variable EXECUTOR_SCRIPT_PATH is not set.")
            exit(1)

    # Use environment variable or script argument for build script file
    script_file = args.script

    # Add environment variables or other context values here
    context = {
        "no_stop": args.no_stop,
    }

    execute_script(script_file, context)
