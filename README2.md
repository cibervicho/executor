## executor - A Simple Script DSL for Task Automation

**executor** is a Python program that provides a **Domain-Specific Language (DSL)** for defining and executing tasks in an automation process. It allows you to create structured scripts using YAML files, where you can specify tasks with dependencies and conditions.

**What can you do with executor?**

* Define tasks with commands, arguments, dependencies, and enabled/disabled states.
* Automate repetitive build processes or workflows.
* Manage complex task execution flows with conditional logic (future implementation).
* Log task execution details (command, output, error) for debugging purposes.

**Prerequisites:**

* Python 3 installed on your system.

**Setting Up the Environment:**

1. **Clone the Project:**

   Use Git to clone the executor project repository from a version control platform like GitHub. You can use the following command in your terminal:

   ```bash
   git clone https://<github_url>/executor.git
   ```

   Replace `<github_url>` with the actual URL of the executor repository.

2. **Create a Virtual Environment (Optional):**

   (This step is optional, but recommended to isolate project dependencies)

   Open a terminal, navigate to the cloned `executor` directory, and create a virtual environment using `venv`:

   ```bash
   python3 -m venv venv
   ```

   This creates a virtual environment directory named `venv`.

   Activate the virtual environment:

   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate.bat  # Windows
   ```

3. **Install Dependencies:**

   (Only necessary if using a virtual environment)

   With the virtual environment activated, install the required dependencies listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

**Building the Executor Binary:**

1. **Build the Executable:**

   Once the dependencies are installed (if using a virtual environment), you can build the standalone executable binary using `pyinstaller`.

   Open the terminal within the project directory and run the following command:

   ```bash
   pyinstaller --onefile executor.py
   ```

   The `--onefile` flag instructs pyinstaller to create a single executable file for better user experience.

   This command will create a new directory named `dist` within your current directory. The `dist` directory contains the generated executable file. The filename will be `executor.exe` on Windows systems and `executor` on Linux/macOS systems.

**Running the Executor:**

Once you have built the executable, you can run it from the command line by providing the path to your YAML script file:

```bash
./dist/executor script.yaml  # For Linux/macOS (replace script.yaml with your actual filename)
dist\executor script.yaml    # For Windows (replace script.yaml with your actual filename)
```

**Alternatively:**

You can set an environment variable to store the script path and use the `-e` option with the executable:

```bash
export SCRIPT_PATH=path/to/your/script.yaml  # Set environment variable
./dist/executor -e SCRIPT_PATH  # For Linux/macOS
dist\executor -e SCRIPT_PATH    # For Windows
```

**Writing Your Script (YAML format):**

The executor uses YAML files to define your automation tasks. Here's a basic example:

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
  dependencies:
    - hello
    - bye
```

This script defines three tasks: `hello`, `bye`, and `hello2`. Each task has a `command` to be executed, optional `arguments`, an `enabled` state, and a list of `dependencies` (optional).

**Additional Notes:**

* The script supports passing a `context` dictionary to the `execute_script` function. This allows you to provide values for arguments used within tasks or for any conditional logic defined in your tasks (future implementation).
* The script logs task execution details (command, standard output, standard error) to a file named `executor_log.txt` located in the same directory as the script.

**Further Development:**

* Implement conditional logic support within tasks for more flexible workflows.
* Enhance task definition syntax for greater flexibility.

**Conclusion:**

`executor` offers a convenient way to manage build automation tasks through a user-friendly YAML syntax. With its features like dependencies, conditions, and logging, it can help automate and streamline your build workflow.

==========================================================

## executor - A Simple Script DSL for Task Automation (Continued)

**Running the Executor with Script from Scratch**

Here's how to clone the project, create a script, and run the executor to generate a result:

1. **Clone the Project (as before):**

   ```bash
   git clone https://<github_url>/executor.git
   ```

2. **Create a Script (example.yaml):**

   Create a new file named `example.yaml` inside the project directory with the following content:

   ```yaml
   task1:
     command: python write_file.py "This is from task 1" output.txt
     enabled: True

   task2:
     command: cat output.txt
     enabled: True
     dependencies:
       - task1
   ```

   This script defines two tasks:

   * `task1`: Uses a Python script (`write_file.py`) to write a message ("This is from task 1") to a file named `output.txt`.
   * `task2`: Uses the `cat` command to print the contents of `output.txt`. 
   * `task2` depends on `task1` completing first.

   **Note:** You'll need to create a separate Python script named `write_file.py` with the following content to fulfill the example task:

   ```python
   import sys

   message = sys.argv[1]
   filename = sys.argv[2]

   with open(filename, "w") as f:
       f.write(message)

   print(f"Successfully wrote message to {filename}")
   ```

3. **Build the Executable (as before):**

   ```bash
   pyinstaller --onefile executor.py
   ```

4. **Run the Executor:**

   Execute the built binary along with your script path:

   ```bash
   ./dist/executor example.yaml  # For Linux/macOS
   dist\executor example.yaml    # For Windows
   ```

   **OR**

   Set the script path in an environment variable and use the `-e` option:

   ```bash
   export SCRIPT_PATH=path/to/your/project/example.yaml  # Set environment variable
   ./dist/executor -e SCRIPT_PATH  # For Linux/macOS
   dist\executor -e SCRIPT_PATH    # For Windows
   ```

   If successful, the script will run `task1`, write the message to `output.txt`, and then `task2` will print the contents of the file. You should see the message "This is from task 1" printed in your terminal.

**Remember:**

* Replace `<github_url>` with the actual URL of the executor repository if you haven't already cloned it.
* Adjust the script path in the `export` command if you saved the script in a different location.
* Make sure you have the `write_file.py` script in the same directory as your `example.yaml` script.

This example demonstrates how to use the `executor` to execute a simple workflow with dependent tasks. With further development of the script and additional tasks, you can automate more complex processes.
