# factorial.py: Calculate Factorials of Large Numbers

This Python program, `factorial.py`, calculates the factorial of a given non-negative integer. The factorial of a number `n` is the product of all positive integers less than or equal to `n`. 

## **Understanding Factorials:**

* Factorial is denoted by `n!`. For example, 5! (factorial of 5) is 5 * 4 * 3 * 2 * 1, which equals 120.
* Factorials are used in various mathematical applications, including probability theory, combinatorics, and recursion.

## **How it Works:**

1. **Importing Libraries:**
    * The program imports necessary modules:
        * `sys`: Provides access to system parameters and functions, used for command-line arguments.
        * `time`: Used for measuring execution time.
        * `gmpy2`: A library specifically designed for high-precision arithmetic with large integers, used for accurate factorial calculations.

2. **`calculate_factorial` Function:**
    * This function takes a non-negative integer `n` as input.
    * It checks if `n` is negative. If so, it raises a `ValueError` as factorials are not defined for negative numbers.
    * It uses `gmpy2` for efficient and accurate calculation, especially for large factorials. It initializes a variable `result` with `mpz(1)` (using `gmpy2` for big integers).
    * It iterates through a loop from 1 to `n`, multiplying the current value of `result` with each number in the sequence. `gmpy2` ensures accurate multiplication even for very large values.
    * To simulate a time-consuming calculation (optional), a small `sleep` is added within the loop (adjust as needed).
    * Finally, the function returns the calculated factorial (`result`).

3. **`main` Function:**
    * This function handles command-line arguments and performs the calculation.
    * It checks if at least one argument (number) is provided. If not, it provides usage instructions and exits.
    * It retrieves the number argument and converts it to an integer using `int(sys.argv[1])`.
    * It validates the number (non-negative) and raises a `ValueError` if it's negative.
    * It measures the execution time using `time.time()` before and after the calculation.
    * It calls the `calculate_factorial` function to compute the factorial.
    * It prints the factorial result, execution time (formatted to three decimal places), and handles any potential `ValueError` exceptions that might occur during calculation.

## **Running the Program:**

1. **Prerequisites:**
    * You need Python 3 installed on your system.
    * Install the `gmpy2` library using `pip install gmpy2`.
2. **Command Line:**
    * Open a terminal or command prompt and navigate to the directory where you saved `factorial.py`.
    * Run the program with the number as an argument:

    ```bash
    python factorial.py <number>
    ```

    Replace `<number>` with the non-negative integer for which you want to calculate the factorial.

**Example:**

```
python factorial.py 5
Factorial of 5 is 120.
Execution time: 0.001 seconds
```

**Large Numbers and `gmpy2`:**

This program utilizes `gmpy2` for accurate calculations of factorials, especially for large numbers. Standard Python integer types might overflow for very large factorials. `gmpy2` provides high-precision arithmetic capabilities to handle such cases effectively.
