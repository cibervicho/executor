import sys

ALLOWED_ARGUMENTS = ["hello", "bye"]

def usage(script_name):
    print(f"Usage: python {script_name} [hello|bye]")
    sys.exit(1)


def validate_args(args):
    if len(args) == 1:
        print("ERROR: No arguments provided.")
        usage(args[0])
    elif len(args) > 2:
        print("ERROR: Too many arguments provided. Expecting one argument.")
        usage(args[0])
    elif len(args) == 2 and args[1] not in ALLOWED_ARGUMENTS:
        print(f"ERROR: Invalid argument: '{args[1]}'. Expected 'hello' or 'bye'.")
        usage(args[0])
    else:
        print(f"Argument '{args[1]}' valid!")


def say_hello():
    print("Hello, world!")


def say_bye():
    print("Goodbye, world!")


if __name__ == "__main__":
    print("Argument List:", sys.argv)
    args = sys.argv[:]
    validate_args(args)

    if args[1].lower() == ALLOWED_ARGUMENTS[0]:
        say_hello()
    elif args[1].lower() == ALLOWED_ARGUMENTS[1]:
        say_bye()
    else:
        print(f"ERROR: Invalid argument: '{args[1]}'. Expected 'hello' or 'bye'.")