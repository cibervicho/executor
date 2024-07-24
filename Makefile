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
	@echo "  clean		- Cleans build artifacts"
	@echo "  build		- Builds the executor binary"
	@echo "  run		- Runs the executor script (requires script.yaml)"
	@echo "  test		- Runs the unit tests using pytest"
	@echo ""
	@echo "  docker-clean	- Removes the executor-app and intermediate docker images"
	@echo "  docker-build	- Builds the executor-app docker image"
	@echo "  docker-run	- Runs the executor-app docker container"

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
	export EXECUTOR_SCRIPT_PATH=$(LOCAL_SCRIPT_YAML) && ./dist/executor

# Run all unit tests using pytest
test:
	pytest test_script_functions.py test_task_class.py -v


### Docker Stuff ###
docker-clean:
ifeq ($(shell docker images -f reference=executor-app:latest | grep -wc executor-app),0)
  # Image doesn't exist, skip cleaning
else
	sudo docker rmi executor-app
	sudo docker builder prune -f
endif

docker-build: docker-clean
	sudo docker build -t executor-app .

docker-run: #docker-build
	@echo " --> $(TARGET)"
	sudo docker run \
		--interactive --tty --rm \
		--volume ./examples:/app/executor \
		--volume ./log:/app/executor/log \
		--env EXECUTOR_SCRIPT_PATH=$(TARGET) \
		executor-app

# To execute the container with an example test just run it as follows:
# 	1. make docker-run TARGET=write_read/write_read.yaml
#   2. make docker-run
#
# Notice that, in 1, we are omitting the 'examples' directory where the test
# resides.
# In 2, we are using the default 'hello world' example.
