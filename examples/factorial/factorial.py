import sys
import time
from gmpy2 import mpz

def calculate_factorial(n):
  """
  Calculates the factorial of a given number using gmpy2 for large integers.

  Args:
      n (mpz): The non-negative integer for which to calculate the factorial.

  Returns:
      mpz: The factorial of n.

  Raises:
      ValueError: If n is negative.
  """
  if n < 0:
    raise ValueError("Factorial is not defined for negative numbers.")
  
  result = mpz(1)
  for i in range(1, n + 1):
    result *= mpz(i)
    # Simulate additional workload with a small sleep (adjust as needed)
    time.sleep(0.001)
  return result

def main():
  """
  Main function to handle command-line arguments and perform calculation.
  """
  # Check for at least one argument (number)
  if len(sys.argv) < 2:
    print("Usage: python factorial.py <number>")
    sys.exit(1)

  # Get the number argument
  try:
    number = int(sys.argv[1])
    # Validate the number (non-negative)
    if number < 0:
      raise ValueError("Factorial is not defined for negative numbers.")
  except ValueError as e:
    print(f"Invalid argument: {e}")
    print("Please provide a non-negative integer.")
    sys.exit(1)

  try:
    start_time = time.time()
    factorial_result = calculate_factorial(number)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Factorial of {number} is {factorial_result}.")
    print(f"Execution time: {execution_time:.3f} seconds")
  except ValueError as e:
    print(e)

if __name__ == "__main__":
  main()
