# **executor - How to run the examples**

The **examples** directory has the following directory structure:
```
examples/
├── README.md
├── ascii_art
│   ├── README.md
│   ├── ascii_art.c
│   └── ascii_art.yaml
├── factorial
│   ├── README.md
│   ├── factorial.py
│   └── factorial.yaml
├── hello
│   ├── README.md
│   ├── hello.py
│   └── hello.yaml
└── write_read
    ├── README.md
    ├── read_from_file.py
    ├── write_read.yaml
    └── write_to_file.py
```

Each subdirectory contains a README file with details about the contents of the particular example itself.

However, here we are going to explain how to execute each example via Docker and/or Python:

## Docker Example Execution

Be sure to run the following commands from the main **executor**'s directory: 

### **hello** Example
```
$ make docker-run TARGET=hello/hello.yaml
 --> hello/hello.yaml
sudo docker run \
        --interactive --tty --rm \
        --volume ./examples:/app/executor \
        --volume ./log:/app/executor/log \
        --env EXECUTOR_SCRIPT_PATH=hello/hello.yaml \
        executor-app
Script 'hello/hello.yaml' structure is valid.
Task 'hello' command: python hello.py hello
Task 'hello' completed successfully.
Task 'bye' skipped since it is disabled.
Task 'echo' depends on incomplete task 'bye'
Task 'release' command: cat /etc/os-release
Task 'release' completed successfully.
```

### **ascii_art** Example
```
$ make docker-run TARGET=ascii_art/ascii_art.yaml
 --> ascii_art/ascii_art.yaml
sudo docker run \
        --interactive --tty --rm \
        --volume ./examples:/app/executor \
        --volume ./log:/app/executor/log \
        --env EXECUTOR_SCRIPT_PATH=ascii_art/ascii_art.yaml \
        executor-app
Script 'ascii_art/ascii_art.yaml' structure is valid.
Task 'validating' command: test -f ascii_art.c
Task 'validating' completed successfully.
Task 'compilation' command: gcc ascii_art.c -o ascii_generator
Task 'compilation' completed successfully.
Task 'execution' command: ./ascii_generator
Task 'execution' completed successfully.
Task 'cleanup' command: rm ascii_generator
Task 'cleanup' completed successfully.
```

### **factorial** Example
```
$ make docker-run TARGET=factorial/factorial.yaml
 --> factorial/factorial.yaml
sudo docker run \
        --interactive --tty --rm \
        --volume ./examples:/app/executor \
        --volume ./log:/app/executor/log \
        --env EXECUTOR_SCRIPT_PATH=factorial/factorial.yaml \
        executor-app
Script 'factorial/factorial.yaml' structure is valid.
Task 'factorial-1' command: python factorial.py 1
Task 'factorial-1' completed successfully.
Task 'factorial-10' command: python factorial.py 10
Task 'factorial-10' completed successfully.
Task 'factorial-100' command: python factorial.py 100
Task 'factorial-100' completed successfully.
Task 'factorial-1000' command: python factorial.py 1000
Task 'factorial-1000' completed successfully.
```

### **write_read** Example
```
$ make docker-run TARGET=write_read/write_read.yaml
 --> write_read/write_read.yaml
sudo docker run \
        --interactive --tty --rm \
        --volume ./examples:/app/executor \
        --volume ./log:/app/executor/log \
        --env EXECUTOR_SCRIPT_PATH=write_read/write_read.yaml \
        executor-app
Script 'write_read/write_read.yaml' structure is valid.
Task 'write' command: python write_to_file.py test.txt This is a test
Task 'write' completed successfully.
Task 'testing' command: test -f test.txt
Task 'testing' completed successfully.
Task 'showing' command: cat test.txt
Task 'showing' completed successfully.
Task 'read' command: python read_from_file.py test.txt This is a test
Task 'read' completed successfully.
Task 'tearDown' command: rm test.txt
Task 'tearDown' completed successfully.
```

## Python Example Execution

First you have to enable the virtual environment and install the requirements:

```bash
python3 -m venv .env

source .env/bin/activate

(.env) pip install -r requirements.txt
```

Execute the python's `executor`'s command, passing the appropriate argument, depending on the example you wish to run

### **hello** Example
```
(.env) python executor.py examples/hello/hello.yaml
Script 'hello/hello.yaml' structure is valid.
Task 'hello' command: python hello.py hello
Task 'hello' completed successfully.
Task 'bye' skipped since it is disabled.
Task 'echo' depends on incomplete task 'bye'
Task 'release' command: cat /etc/os-release
Task 'release' completed successfully.
```

### **ascii_art** Example
```
(.env) python executor.py examples/ascii_art/ascii_art.yaml
Script 'examples/ascii_art/ascii_art.yaml' structure is valid.
Task 'validating' command: test -f ascii_art.c
Task 'validating' completed successfully.
Task 'compilation' command: gcc ascii_art.c -o ascii_generator
Task 'compilation' completed successfully.
Task 'execution' command: ./ascii_generator
Task 'execution' completed successfully.
Task 'cleanup' command: rm ascii_generator
Task 'cleanup' completed successfully.
```

### **factorial** Example
```
(.env) python executor.py examples/factorial/factorial.yaml
Script 'factorial/factorial.yaml' structure is valid.
Task 'factorial-1' command: python factorial.py 1
Task 'factorial-1' completed successfully.
Task 'factorial-10' command: python factorial.py 10
Task 'factorial-10' completed successfully.
Task 'factorial-100' command: python factorial.py 100
Task 'factorial-100' completed successfully.
Task 'factorial-1000' command: python factorial.py 1000
Task 'factorial-1000' completed successfully.
```

### **write_read** Example
```
(.env) python executor.py examples/write_read/write_read.yaml
Script 'write_read/write_read.yaml' structure is valid.
Task 'write' command: python write_to_file.py test.txt This is a test
Task 'write' completed successfully.
Task 'testing' command: test -f test.txt
Task 'testing' completed successfully.
Task 'showing' command: cat test.txt
Task 'showing' completed successfully.
Task 'read' command: python read_from_file.py test.txt This is a test
Task 'read' completed successfully.
Task 'tearDown' command: rm test.txt
Task 'tearDown' completed successfully.
```
