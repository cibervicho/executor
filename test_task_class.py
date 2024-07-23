# test_task_class.py

import os
import pytest
from unittest.mock import patch

from executor import Task


@pytest.fixture
def task_with_command(name="test_task", command="echo hello"):
    return Task(name, command)


@pytest.fixture
def task_with_arguments(name="test_task", command="echo", arguments={"name": "world"}):
    return Task(name, command, arguments)


@pytest.fixture
def task_with_dependencies(name="test_task", command="echo hello", dependencies=["dep1", "dep2"]):
    return Task(name, command, dependencies=dependencies)


def test_task_init(task_with_command):
    """
    Test Task object initialization with name and command.
    """
    assert task_with_command.name == "test_task"
    assert task_with_command.command == "echo hello"
    assert task_with_command.arguments == {}
    assert task_with_command.dependencies == []
    assert task_with_command.enabled is True
    assert task_with_command.test_dir == ""


def test_task_with_arguments(task_with_arguments):
    """
    Test Task object initialization with arguments.
    """
    assert task_with_arguments.arguments == {"name": "world"}


def test_task_with_dependencies(task_with_dependencies):
    """
    Test Task object initialization with dependencies.
    """
    assert task_with_dependencies.dependencies == ["dep1", "dep2"]


@patch("subprocess.Popen")
def test_task_execute_success(mock_popen, task_with_command):
    """
    Test successful task execution using mocked subprocess.Popen.
    """
    mock_process = mock_popen.return_value
    mock_process.returncode = 0
    mock_process.communicate.return_value = (b"Output message", b"")

    task_with_command.test_dir = os.getcwd()
    retcode, output, error = task_with_command.execute({})

    assert retcode == 0
    assert output == "Output message"
    assert error == ""
    mock_popen.assert_called_once()


@patch("subprocess.Popen")
def test_task_execute_failure(mock_popen, task_with_command):
    """
    Test task execution failure using mocked subprocess.Popen.
    """
    mock_process = mock_popen.return_value
    mock_process.returncode = 1
    mock_process.communicate.return_value = (b"Error message", b"")

    task_with_command.test_dir = os.getcwd()
    retcode, output, error = task_with_command.execute({})

    assert retcode == 1
    assert output == "Error message"
    assert error == ""
    mock_popen.assert_called_once()
