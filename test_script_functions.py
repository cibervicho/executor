# test_script_functions.py

import pytest
from unittest.mock import patch

from executor import read_script, validate_script, get_all_tasks, Task


@pytest.fixture
def valid_script_content():
    return """
task1:
  command: echo hello
  arguments:
    name: world
task2:
  command: cat output.txt
  dependencies:
    - task1
"""


@pytest.fixture
def valid_script_dict(valid_script_content):
    return read_script(valid_script_content)


def test_read_script_success(tmp_path, valid_script_content):
    """
    Test reading a valid YAML script using a temporary file.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    script_dict = read_script(str(script_file))
    assert script_dict == read_script(valid_script_content)


def test_read_script_file_not_found():
    """
    Test raising an error for a non-existent script file.
    """
    with pytest.raises(FileNotFoundError):
        read_script("non-existent.yaml")


def test_read_script_yaml_error(tmp_path):
    """
    Test raising an error for invalid YAML syntax.
    """
    invalid_content = "invalid_yaml_content"
    script_file = tmp_path / "invalid.yaml"
    script_file.write_text(invalid_content)

    with pytest.raises(YAMLError):
        read_script(str(script_file))


def test_validate_script_success(valid_script_dict):
    """
    Test successful validation of a valid script structure.
    """
    validate_script(valid_script_dict)


def test_validate_script_missing_command(valid_script_dict):
    """
    Test raising an error for a task missing the required 'command' key.
    """
    del valid_script_dict["task1"]["command"]
    with pytest.raises(ValueError) as excinfo:
        validate_script(valid_script_dict)

    assert "Task 'task1' is missing required key 'command'" in str(excinfo.value)


def test_validate_script_invalid_dependency(valid_script_dict):
    """
    Test raising an error for a task with a non-existent dependency.
    """
    valid_script_dict["task1"]["dependencies"] = ["non_existent_task"]
    with pytest.raises(ValueError) as excinfo:
        validate_script(valid_script_dict)

    assert "Task 'task1' has an invalid dependency: 'non_existent_task'" in str(excinfo.value)


def test_get_all_tasks(valid_script_dict):
    """
    Test extracting all tasks as Task objects from the script dictionary.
    """
    tasks = get_all_tasks(valid_script_dict)
    assert len(tasks) == 2
    assert isinstance(tasks[0], Task) and tasks[0].name == "task1"
    assert isinstance(tasks[1], Task) and tasks[1].name == "task2"


@patch("executor.Task.execute")
def test_execute_script_success(mock_task_execute, tmp_path, valid_script_content):
    """
    Test successful execution of the script with mocked task execution.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.return_value = (0, None, None)  # Simulate successful task execution

    retcode, output, error = execute_script(str(script_file))

    assert retcode == 0
    assert output is None
    assert error is None
    mock_task_execute.assert_called()  # Verify all tasks were executed


@patch("executor.Task.execute")
def test_execute_script_failure(mock_task_execute, tmp_path, valid_script_content):
    """
    Test script execution failure with mocked task execution.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.side_effect = [(-1, "Error message", None), (0, None, None)]  # Simulate task execution failure

    retcode, output, error = execute_script(str(script_file))

    assert retcode == -1
    assert output == "Error message"
    assert error is None
    mock_task_execute.assert_called_with("task1")  # Verify only task1 was executed



@patch("executor.Task.execute")
def test_execute_script_skip_failed_tasks(mock_task_execute, tmp_path, valid_script_content):
    """
    Test skipping failed tasks when executing the script.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.side_effect = [(-1, "Error message", None), (0, None, None)]  # Simulate task execution failure

    retcode, output, error = execute_script(str(script_file), skip_failed_tasks=True)

    assert retcode == 0
    assert output is None
    assert error is None
    mock_task_execute.assert_called_once_with("task1")  # Verify only task1 was executed


@patch("executor.Task.execute")
def test_execute_script_stop_on_failure(mock_task_execute, tmp_path, valid_script_content):
    """
    Test stopping the execution of the script when a task fails.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.side_effect = [(-1, "Error message", None), (1, None, None)]  # Simulate task execution failure

    retcode, output, error = execute_script(str(script_file), stop_on_failure=True)

    assert retcode == 1
    assert output == "Error message"
    assert error is None
    mock_task_execute.assert_called_with("task1")  # Verify only task1 was executed



@patch("executor.Task.execute")
def test_execute_script_exit_code_threshold(mock_task_execute, tmp_path, valid_script_content):
    """
    Test stopping the execution of the script when the exit code threshold is reached.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.side_effect = [(0, None, None), (1, None, None), (2, None, None)]  # Simulate task execution failure

    retcode, output, error = execute_script(str(script_file), exit_code_threshold=2)

    assert retcode == 2
    assert output is None
    assert error is None
    mock_task_execute.assert_called_with("task1")  # Verify only task1 was executed


@patch("executor.Task.execute")
def test_execute_script_max_attempts(mock_task_execute, tmp_path, valid_script_content):
    """
    Test stopping the execution of the script when the maximum number of attempts is reached.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.side_effect = [(-1, "Error message", None)] * 3  # Simulate task execution failure

    retcode, output, error = execute_script(str(script_file), max_attempts=3)

    assert retcode == -1
    assert output == "Error message"
    assert error is None
    mock_task_execute.assert_called_with("task1")  # Verify only task1 was executed


@patch("executor.Task.execute")
def test_execute_script_retry_delay(mock_task_execute, tmp_path, valid_script_content):
    """
    Test retrying failed tasks with a specific delay between attempts.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.side_effect = [(-1, "Error message", None), (0, None, None)]  # Simulate task execution failure

    retcode, output, error = execute_script(str(script_file), retry_delay=1)

    assert retcode == 0
    assert output is None
    assert error is None
    mock_task_execute.assert_called_with("task1", delay=1)  # Verify task1 was retried with a delay


@patch("executor.Task.execute")
def test_execute_script_max_retry_delay(mock_task_execute, tmp_path, valid_script_content):
    """
    Test stopping retrying failed tasks when the maximum retry delay is reached.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.side_effect = [(-1, "Error message", None)] * 3  # Simulate task execution failure

    retcode, output, error = execute_script(str(script_file), max_retry_delay=1)

    assert retcode == -1
    assert output == "Error message"
    assert error is None
    mock_task_execute.assert_called_with("task1")  # Verify only task1 was executed


@patch("executor.Task.execute")
def test_execute_script_custom_exit_code_handler(mock_task_execute, tmp_path, valid_script_content):
    """
    Test handling custom exit codes.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.side_effect = [(0, None, None), (1, None, None), (2, None, None)]  # Simulate task execution failure

    retcode, output, error = execute_script(str(script_file), exit_code_handler=lambda x: x > 1)

    assert retcode == 2
    assert output is None
    assert error is None
    mock_task_execute.assert_called_with("task1")  # Verify only task1 was executed


@patch("executor.Task.execute")
def test_execute_script_custom_task_handler(mock_task_execute, tmp_path, valid_script_content):
    """
    Test handling custom task execution.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.return_value = (0, None, None)  # Simulate successful task execution

    retcode, output, error = execute_script(str(script_file), task_handler=lambda x: x.name == "task1")

    assert retcode == 0
    assert output is None
    assert error is None
    mock_task_execute.assert_called_with("task1")  # Verify only task1 was executed


@patch("executor.Task.execute")
def test_execute_script_custom_log_handler(mock_task_execute, tmp_path, valid_script_content):
    """
    Test handling custom logging.
    """
    script_file = tmp_path / "test.yaml"
    script_file.write_text(valid_script_content)

    mock_task_execute.return_value = (0, None, None)  # Simulate successful task execution

    with patch("executor.logger.info") as mock_logger_info:
        execute_script(str(script_file), log_handler=mock_logger_info)

        mock_logger_info.assert_called_with("Executing task: task1")  # Verify logging occurred
    
