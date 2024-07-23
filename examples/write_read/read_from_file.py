import os
import sys

def validate_input(filename, content):
  """
  Validates the input filename and content.

  Args:
      filename (str): The filename provided as an argument.
      content (str): The content provided as an argument.

  Raises:
      ValueError: If the filename is empty or the content is empty.
  """
  if not filename:
    raise ValueError("Error: Please provide a filename.")
  if not content:
    raise ValueError("Error: Please provide content to compare.")

def read_file_content(filename):
  """
  Reads the content of a file.

  Args:
      filename (str): The name of the file to read.

  Returns:
      str: The content of the file.

  Raises:
      FileNotFoundError: If the file is not found.
  """
  try:
    with open(filename, 'r') as file:
      return file.read().strip()
  except FileNotFoundError:
    raise FileNotFoundError(f"Error: File '{filename}' not found.")

def main():
  """
  Main function to handle script execution.
  """
  # Check for at least two arguments (filename and content)
  if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} <filename> <content>")
    sys.exit(1)

  filename = os.path.join(os.getcwd(), sys.argv[1])
  content = " ".join(sys.argv[2:])

  # Validate input arguments
  try:
    validate_input(filename, content)
  except ValueError as e:
    print(e)
    sys.exit(1)

  # Read file content
  try:
    file_content = read_file_content(filename)
  except FileNotFoundError as e:
    print(e)
    sys.exit(1)

  # Compare file content with provided content
  if file_content != content:
    print(f"Error: Content in '{filename}' does not match the provided content.")
    sys.exit(1)
  else:
    print("Success: Content in the file matches the provided content.")

if __name__ == "__main__":
  main()
