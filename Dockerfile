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
    apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY build_bots.py /app/build_bots.py
COPY run_bots.py /app/run_bots.py
COPY bots_config.json /app/bots_config.json
COPY requirements.txt /app/requirements.txt
COPY README.md /app/README.md

# Make the scripts executable
RUN chmod +x /app/build_bots.py /app/run_bots.py

# Install Python dependencies
RUN pip3 install -r requirements.txt

# If build_bots.py installs dependencies, run it here
RUN python3 build_bots.py

# Define the default command to run when the container starts
CMD ["python3", "run_bots.py"]
