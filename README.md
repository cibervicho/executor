**executor - A Simple Script DSL**

**What is executor?**

`executor` is a Python program that provides a **Domain-Specific Language (DSL)** for defining and executing tasks in an automation process. It allows you to create structured scripts using YAML files, where you can specify tasks with dependencies and conditions.

**Key Features:**

- **YAML Support:** Tasks are defined within a YAML file, making the script human-readable and easy to maintain.
- **Dependencies:** Tasks can specify dependencies on other tasks, ensuring that dependent tasks are executed only after their dependencies are completed.
- **Conditions:** Tasks can include conditional statements using Python expressions. A task will only be executed if its condition evaluates to `True`.
- **Command Execution:** Tasks execute shell commands through Python's `subprocess` module.
- **Logging:** The program logs task execution details, including standard output, standard error, timestamps, and return codes, to a file named `executor_log.txt`.

**How to Use executor**

1. **Define Your Script:**
   - Create a YAML file containing your build tasks. Here's an example structure:

   ```yaml
   task1:
       command: python build_script.py task1_arguments
       # ... (optional dependencies and conditions)

   task2:
       command: python build_script.py task2_arguments
       dependencies:
           - task1  # Task2 depends on the successful completion of task1
   ```

2. **Run the Script:**
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

**Context (Optional):**

You can optionally define a `context` dictionary in the script to provide values for arguments and condition evaluation within your tasks.

**Example Usage:**

Consider the following YAML script (`build_script.yaml`):

```yaml
clean:
    command: rm -rf *.pyc

build:
    command: python setup.py build
    dependencies:
        - clean

test:
    command: python -m unittest test*.py
    dependencies:
        - build

deploy:
    command: scp dist/* user@host:/path/to/deployment/dir
    condition: 'env.get("DEPLOY", False)'  # Only deploy if DEPLOY environment variable is set to True
    dependencies:
        - test
```

Running `python executor.py build_script.yaml` would execute the tasks in the following order:

1. `clean` (removes Python bytecode files)
2. `build` (builds the project)
3. `test` (runs unit tests)
4. `deploy` (deploys the build artifacts, but only if the `DEPLOY` environment variable is set to `True`)

**Error Handling and Logging:**

- The program raises errors for missing required keys in task definitions and invalid YAML files.
- It logs task execution details (command, output, error, timestamp, return code) to `executor_log.txt` to aid in debugging.

**Conclusion:**

`executor` offers a convenient way to manage build automation tasks through a user-friendly YAML syntax. With its features like dependencies, conditions, and logging, it can help automate and streamline your build workflow.
