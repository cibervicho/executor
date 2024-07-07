**executor - A Simple Script DSL**

**What is executor?**

`executor` is a Python program that provides a **Domain-Specific Language (DSL)** for defining and executing tasks in an automation process. It allows you to create structured scripts using YAML files, where you can specify tasks with dependencies and conditions.

**Key Features:**

- **YAML Support:** Tasks are defined within a YAML file, making the script human-readable and easy to maintain.
- **Dependencies:** Tasks can specify dependencies on other tasks, ensuring that dependent tasks are executed only after their dependencies are completed.
- **Conditions:** Tasks can include conditional statements using Python expressions. A task will only be executed if its condition evaluates to `True`.
- **Command Execution:** Tasks execute shell commands through Python's `subprocess` module.
- **Logging:** The program logs task execution details, including standard output, standard error, timestamps, and return codes, to a file named `executor_log.txt`.

**General Features:**

- Define tasks with commands, arguments, dependencies, and enabled/disabled states.
- Validate script structure for required keys and data types.
- Execute tasks based on completion of dependencies and enabled status.
- Handle task execution failures and display informative messages.
- Log task execution details (command, output, error) to a file.
- Support optional arguments for tasks (arguments).
- Support task dependencies for defining execution order (dependencies).

**How to Use executor**

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .env
   ```

   ```bash
   source .env/bin/activate
   ```

2. **Install dependencies in your virtual environment:**
    ```bash
   (.env) pip install -r requirements.txt
   ```

3. **Define Your Script:**
   - Create a YAML file containing your build tasks. Here's an example structure:

   ```yaml
   hello:
        command: python hello.py {argument}
        enabled: True
        arguments:
            argument: hello

    bye:
        command: python hello.py {argument}
        enabled: True
        arguments:
            argument: bye
        dependencies:
            - hello  # bye depends on hello completing first

    hello2:
        command: python hello.py hello
        enabled: True
        dependencies:  # hello2 depends on hello and bye completing first
            - hello
            - bye
   ```

4. **Run the Script:**
   - Open a terminal and navigate to the directory containing your YAML script and `executor.py`.
   - Execute the program using the following command:

   ```bash
   python executor.py script.yaml  # Replace "script.yaml" with your actual filename
   ```

   - Alternatively, you can set an environment variable to store the script path and use the `-e` option:

   ```bash
   export SCRIPT_PATH=path/to/your/script.yaml
   python executor.py -e SCRIPT_PATH
   ```

**Optional Arguments:**

- `-e`, `--env`: Specifies the environment variable containing the script path (avoids providing the path directly).
- `--no-stop`: Instructs the program to continue execution even if a task fails (default behavior is to stop).

**Context:**

The script supports passing a `context` dictionary to the execute_script function. This allows you to provide values for arguments used within tasks or for any conditional logic defined in your tasks.

**Logging**:

The script logs task execution details (command, standard output, standard error) to a file named `executor_log.txt` located in the same directory as the script.

**Further Development**:

- Implement conditional logic support within tasks.
- Enhance task definition syntax for greater flexibility.

**Error Handling and Logging:**

- The program raises errors for missing required keys in task definitions and invalid YAML files.
- It logs task execution details (command, output, error, timestamp, return code) to `executor_log.txt` to aid in debugging.

**Conclusion:**

`executor` offers a convenient way to manage build automation tasks through a user-friendly YAML syntax. With its features like dependencies, conditions, and logging, it can help automate and streamline your build workflow.
