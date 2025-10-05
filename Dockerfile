# Use an official base image
FROM ubuntu:20.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
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

# Set working directory
WORKDIR /tmp/app

# Copy project files
COPY build_bots.py /app/build_bots.py
COPY run_bots.py /app/run_bots.py
COPY bots_config.json /app/bots_config.json
COPY requirements.txt /app/requirements.txt
COPY README.md /app/README.md

# Change ownership
RUN chown -R appuser:appgroup /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER 10014

# Clone and run bots when container starts (not during build)
CMD bash -c "python3 build_bots.py && python3 run_bots.py"
