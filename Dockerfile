# Base image for Python environment
FROM python:3.12-slim as builder

# Update package lists
RUN apt-get update && apt-get upgrade -y

# Install build essentials to have make available
RUN apt-get install -y build-essential

# Set working directory
WORKDIR /app/executor

# Copy required files to build container
COPY requirements.txt Makefile executor.py ./

# Install requirements from requirements.txt
RUN pip install -r requirements.txt

# Build the executor binary
RUN make build


# Target executor Image
FROM python:3.12-slim

# Installing vim for easier navigation of files and compilers
RUN apt-get update && \
    apt-get install \
        vim \
        gcc -y

# Copy the executor and binaries required to the container
COPY --from=builder /app/executor/dist/executor /usr/local/bin/executor
COPY --from=builder /app/executor/requirements.txt /app/executor/requirements.txt

# Install requirements from requirements.txt
RUN pip install -r /app/executor/requirements.txt

# Set the working directory for execution
WORKDIR /app/executor

# Entrypoint command
CMD ["executor"]
