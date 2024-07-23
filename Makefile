# Define variables
PYTHON = python3
PYINSTALLER = pyinstaller
LOCAL_SCRIPT_YAML = ./examples/hello/hello.yaml

TARGET ?= hello/hello.yaml

# Define targets
.PHONY: clean build run help

# Help target
help:
	@echo "Available targets:"
	@echo "  clean		- Clean build artifacts"
	@echo "  build		- Build the executor binary"
	@echo "  run		- Run the executor script (requires script.yaml)"
	@echo "  test		- Run the unit tests using pytest"
	@echo ""
	@echo "  docker-build	- Builds the executor-app docker image"
	@echo "  docker-run	- Run the executor-app docker container"
	@echo "  docker-clean	- Removes the executor-app and intermediate docker images"

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
	./dist/executor $(LOCAL_SCRIPT_YAML)

# Define a target to run the script with an environment variable
run-env: clean build
	export EXECUTOR_SCRIPT_PATH=$(LOCAL_SCRIPT_YAML) && ./dist/executor -e EXECUTOR_SCRIPT_PATH

# Run all unit tests using pytest
test:
	pytest test_script_functions.py test_task_class.py -v


### Docker Stuff ###
docker-build:
	sudo docker build -t executor-app .

docker-run:
	@echo " --> $(TARGET)"
	sudo docker run \
		--interactive --tty --rm \
		--volume ./examples:/app/executor \
		--volume ./log:/app/executor/log \
		--env EXECUTOR_SCRIPT_PATH=$(TARGET) \
		executor-app

docker-clean:
	sudo docker rmi executor-app
	sudo docker builder prune -f

# TODO: Pass those examples to the container through the make command
