# Base image for Python environment
FROM python:3.12-slim as builder

# Update package lists
RUN apt-get update && apt-get upgrade -y

# Install build essentials and git
RUN apt-get install -y build-essential git vim

# Set working directory
WORKDIR /app/executor

# Clone the executor repository
# COPY https://github.com/cibervicho/executor.git .
COPY requirements.txt Makefile executor.py ./

# Install requirements from requirements.txt (optional)
RUN pip install -r requirements.txt

# Build the executor binary (optional)
# Assuming a Makefile with a 'build' target exists
RUN make build


FROM bitnami/python:3.12.4-debian-12-r4

# Copy the executor binary to the container (if built)
COPY --from=builder /app/executor/dist/executor /app/executor/executor

# Copy the hello directory and its contents (optional)
COPY hello /app/executor/hello

# Set the working directory for execution (optional)
WORKDIR /app/executor

# Entrypoint command (optional)
# Replace with your actual execution command
CMD ["executor", "hello/hello.yaml"]


#TO Build:
    # docker build -t executor-app .