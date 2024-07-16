# Define variables
PYTHON = python3
PYINSTALLER = pyinstaller
SCRIPT_YAML = hello/hello.yaml

# Define targets
.PHONY: clean build run help

# Help target
help:
	@echo "Available targets:"
	@echo "  clean  - Clean build artifacts"
	@echo "  build  - Build the executor binary"
	@echo "  run    - Run the executor script (requires script.yaml)"
	@echo "  test   - Run the unit tests using pytest"

# Clean target
clean:
	rm -rf dist build __pycache__ *.egg-info

# Build target
build:
	#$(PYTHON) -m venv venv  # Create virtual environment (optional)
	#source venv/bin/activate  # Activate virtual environment (optional)
	#pip install -r requirements.txt  # Install dependencies (optional)
	$(PYINSTALLER) --onefile executor.py  # Build the executable

# Run target
run: clean build
	./dist/executor $(SCRIPT_YAML)
	
# Define a target to run the script with an environment variable
run-env: clean build
	export EXECUTOR_SCRIPT_PATH=$(SCRIPT_YAML) && ./dist/executor -e EXECUTOR_SCRIPT_PATH

# Run all unit tests using pytest
test:
	pytest test_script_functions.py test_task_class.py -v
