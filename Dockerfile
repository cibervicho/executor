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

# Installing vim for easier navigation of files
RUN apt-get update && apt-get install vim -y

# Copy the executor binary to the container
COPY --from=builder /app/executor/dist/executor /usr/local/bin/executor

# Set the working directory for execution
WORKDIR /app/executor

# Entrypoint command
CMD ["executor"]
