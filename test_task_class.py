# test_task_class.py

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
    assert task_with_command.arguments is None
    assert task_with_command.dependencies == []
    assert task_with_command.enabled is True


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

    retcode, output, error = task_with_command.execute({})

    assert retcode == 0
    assert output.decode() == "Output message"
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

    retcode, output, error = task_with_command.execute({})

    assert retcode == 1
    assert output.decode() == "Error message"
    assert error == ""
    mock_popen.assert_called_once()


@pytest.mark.parametrize("dependencies", [["missing_dep"]])
def test_task_check_dependencies_missing(task_with_dependencies, dependencies):
    """
    Test checking for missing dependencies.
    """
    missing_deps = task_with_dependencies.check_dependencies(dependencies)
    assert missing_deps == dependencies


def test_task_check_dependencies_all_present(task_with_dependencies):
    """
    Test checking for dependencies when all are present.
    """
    missing_deps = task_with_dependencies.check_dependencies(["dep1", "dep2"])
    assert missing_deps == []
