# Use an official base image (e.g., Ubuntu)
FROM ubuntu:20.04

# Set environment variables (if needed for the project)
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies, including python3 and pip3
RUN apt-get update && \
    apt-get install -y \
    bash \
    curl \
    git \
    jq \
    python3 \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user (UID 10014)
RUN groupadd --system appgroup && \
    useradd --system --uid 10014 --gid appgroup --create-home appuser

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY build_bots.py /app/build_bots.py
COPY run_bots.py /app/run_bots.py
COPY bots_config.json /app/bots_config.json
COPY requirements.txt /app/requirements.txt
COPY README.md /app/README.md

# Change ownership of app files to non-root user
RUN chown -R appuser:appgroup /app

# Install Python dependencies as root
RUN pip3 install --no-cache-dir -r requirements.txt

# Run build script as root (if needed for dependencies)
RUN python3 build_bots.py

# Switch to non-root user
USER 10014

# Define the default command to run when the container starts
CMD ["python3", "run_bots.py"]
