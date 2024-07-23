import os
import sys

def validate_filename(filename):
  """
  Validates the filename provided as an argument.

  Args:
      filename (str): The filename provided as an argument.

  Raises:
      ValueError: If the filename is empty.
  """
  if not filename:
    raise ValueError("Error: Please provide a filename.")


def write_to_file(filename, content):
  """
  Writes content to a specified file, performing basic content validation.

  Args:
      filename (str): The name of the file to write to.
      content (str): The content to write to the file.

  Raises:
      ValueError: If the content is empty or contains invalid characters.
  """
  # Validate content (replace with your desired validation logic)
  if not content:
    raise ValueError("Error: Content to write cannot be empty.")
  elif any(char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !@#$%^&*()_+-=[]{};':\"\\|,.<>/?`~" for char in content):
    raise ValueError("Error: Content contains invalid characters.")

  try:
    # Open the file in write mode ('w')
    with open(filename, 'w') as file:
      # Write the content to the file
      file.write(content)
      print(f"Successfully wrote content to {filename}")
  except FileNotFoundError:
    print(f"Error: File '{filename}' could not be created.")

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
    validate_filename(filename)
  except ValueError as e:
    print(e)
    sys.exit(1)

  # Validate content within the write_to_file function
  try:
    write_to_file(filename, content)
  except ValueError as e:
    print(e)
    sys.exit(1)

if __name__ == "__main__":
  main()
