# **executor - A Simple Script DSL**

## **What is executor?**

`executor` is a Python program that provides a **Domain-Specific Language (DSL)** for defining and executing tasks in an automation process. It allows you to create structured scripts using YAML files, where you can specify tasks with dependencies.

### **Key Features:**

- **YAML Support:** Tasks are defined within a YAML file, making the script human-readable and easy to maintain.
- **Dependencies:** Tasks can specify dependencies on other tasks, ensuring that dependent tasks are executed only after their dependencies are completed.
- **Command Execution:** Tasks execute shell commands through Python's `subprocess` module.
- **Logging:** The program logs task execution details, including standard output, standard error, timestamps, and return codes, to a file named `executor_log.txt`.

### **General Features:**

- Define tasks with commands, arguments, dependencies, and enabled/disabled states.
- Validate script structure for required keys and data types.
- Execute tasks based on completion of dependencies and enabled status.
- Handle task execution failures and display informative messages.
- Log task execution details (command, output, error) to a file.
- Support optional arguments for tasks (arguments).
- Support task dependencies for defining execution order (dependencies).

## **`executor`'s Grammar**

The `executor.py` script doesn't define a formal grammar in the traditional sense. However, it does establish a specific syntax for defining tasks within a YAML file:

### **Task Definition:**

* Each task is defined as a key-value pair within the YAML dictionary. The key represents the task name (string).
* The value is a dictionary containing optional and required keys for defining the task's behavior.

### **Required Key:**

* `command` (string): This key specifies the command to be executed for the task. It can include placeholders denoted by curly braces (`{}`) for arguments.

### **Optional Keys:**

* `enabled` (boolean, default: True): This key indicates whether the task is enabled for execution.
* `arguments` (dictionary): This key defines arguments to be passed to the command. The dictionary keys represent argument names, and the values are the corresponding argument values (strings).
* `dependencies` (list of strings): This key lists task names that this task depends on. The task will only be executed if all its dependencies are completed and enabled.

### **Additional Notes:**

* The script uses namedtuples (`TaskDef`) to represent tasks internally. This provides type checking and structure for task definitions.
* The script validates the YAML structure for required keys and data types during script execution.

**Overall, the syntax for defining tasks in the YAML file is relatively simple and human-readable.** It offers a clear way to define task commands, arguments, dependencies, and enabled/disabled states.

## **How to Use executor**

There are 2 different ways to use executor:

1. Using Docker, or
2. Using Python directly.

### `executor` with Docker

**Note that it is assumed that you have Docker installed in your system.**

If you still need to install Docker, you can follow the instructions in the [official documentation](https://docs.docker.com/engine/install/).

This is the easiest way to try `executor`.

1. **Run the command with `make`**
   ```bash
   make docker-run
   ```
   By doing this, the Makefile will build the required image with all it's dependencies, and at the end, will run the following command:
   ```bash
   sudo docker run \
        --interactive --tty --rm \
        --volume ./examples:/app/executor \
        --volume ./log:/app/executor/log \
        --env EXECUTOR_SCRIPT_PATH=hello/hello.yaml \
        executor-app
   ```
   As you can see the default **Hello World** example is used.

   If you want to run a different example, you can use the following command:
   ```bash
   make docker-run TARGET=write_read/write_read.yaml
   ```

2. **Passing different examples**
   If you want to run a different example with docker, you need to create a new directory with your **yaml** configuration file inside of the **examples** directory.

   If your configuration file needs additional scripts, such as python scripts, you have to place them inside the **examples** directory as well.

### `executor` with Python

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
   - Create a YAML file containing your tasks in the `examples` directory. Here's an example structure:

   ```yaml
    hello:
    command: python hello.py {argument}
    arguments:
        argument: hello

    bye:
    command: python hello.py {argument}
    enabled: False
    arguments:
        argument: bye
    dependencies:
        - hello

    echo:
    command: echo $PATH
    dependencies:
        - hello
        - bye

    release:
    command: cat {release_filename}
    arguments:
        release_filename: /etc/os-release
   ```

4. **Run the Script:**
   - Open a terminal and navigate to the directory containing your `executor.py` script.
   - Execute the program using the following command:

   ```bash
   python executor.py examples/script/script.yaml  # Replace "script.yaml" with your actual configuration filename
   ```

   - Alternatively, you can set the `EXECUTOR_SCRIPT_PATH` environment variable to store the script path of your configuration filename, and simply invoke the `executor.py` script:

   ```bash
   export EXECUTOR_SCRIPT_PATH=path/to/your/script.yaml
   python executor.py
   ```

#### **Optional Arguments:**

- `--no-stop`: Instructs the program to continue execution even if a task fails (default behavior is to stop).

### **Logging**:

The script logs task execution details (command, standard output, standard error) to a file named `executor_log.txt` located in the same directory as the script.

## **Further Development**:

- Implement conditional logic support within tasks.
- Enhance task definition syntax for greater flexibility.

## **Error Handling and Logging:**

- The program raises errors for missing required keys in task definitions and invalid YAML files.
- It logs task execution details (command, output, error, timestamp, return code) to `executor_log.txt` to aid in debugging.

## **Conclusion:**

`executor` offers a convenient way to manage build automation tasks through a user-friendly YAML syntax. With its features like dependencies, conditions, and logging, it can help automate and streamline your build workflow.
