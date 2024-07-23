## hello.py - A Script for Greeting Messages

This is a Python script named `hello.py` that allows you to print greeting messages to the console. It takes one argument, either "hello" or "bye", and executes the corresponding function to print a greeting message.

### Usage

```
python hello.py [hello|bye]
```

**Arguments:**

* `hello`: Prints "Hello, world!"
* `bye`: Prints "Goodbye, world!"

**Example:**

```
python hello.py hello
```

This will print:

```
Argument List: ['hello.py', 'hello']
Hello, world!
```

### Script Details

The script consists of several functions:

* `ALLOWED_ARGUMENTS`: This list defines the valid arguments the script accepts ("hello" or "bye").
* `usage(script_name)`: This function prints a usage message with the script name and exits the program with an error code (1).
* `validate_args(args)`: This function validates the provided arguments. It checks for the following conditions:
    * No arguments provided: Exits with an error message and usage instructions.
    * Too many arguments provided: Exits with an error message and usage instructions.
    * Invalid argument provided: Exits with an error message specifying the invalid argument and expected options.
    * Valid argument provided: Prints a success message indicating the validity of the argument.
* `say_hello()`: This function prints the greeting message "Hello, world!".
* `say_bye()`: This function prints the greeting message "Goodbye, world!".
* `if __name__ == "__main__":`: This block executes only when the script is run directly (not imported as a module). It performs the following steps:
    * Prints the list of arguments passed to the script using `sys.argv`.
    * Creates a copy of the argument list (`args`) to avoid modifying the original `sys.argv`.
    * Calls the `validate_args` function to validate the arguments.
    * Checks the first argument (index 1, after script name) in lowercase and compares it with the allowed arguments.
        * If it matches "hello", calls the `say_hello` function.
        * If it matches "bye", calls the `say_bye` function.
        * If it doesn't match any valid argument, prints an error message and exits.
