import os
import subprocess
import json
import sys

# Configuration file
CONFIG_FILE = "bots_config.json"

if not os.path.isfile(CONFIG_FILE):
    print(f"Configuration file {CONFIG_FILE} not found!")
    sys.exit(1)

# Load configuration
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

def build_bot(bot_name, bot_config):
    directory = bot_name
    source = bot_config.get("source")
    branch = bot_config.get("branch", "main")

    # Clone or pull repository
    if not os.path.isdir(directory):
        print(f"Cloning {bot_name} from {source} into {directory}")
        result = subprocess.run(["git", "clone", "--branch", branch, source, directory])
        if result.returncode != 0:
            print(f"Failed to clone {source}")
            sys.exit(1)
    else:
        print(f"Directory {directory} already exists. Pulling latest changes.")
        os.chdir(directory)
        result = subprocess.run(["git", "pull"])
        if result.returncode != 0:
            print(f"Failed to pull latest changes for {directory}")
            sys.exit(1)
        os.chdir("..")

    # Install dependencies
    print(f"Installing dependencies for {bot_name}")
    os.chdir(directory)
    result = subprocess.run(["pip3", "install", "-r", "requirements.txt"])
    if result.returncode != 0:
        print(f"Failed to install dependencies for {bot_name}")
        sys.exit(1)
    os.chdir("..")

def run_bot(bot_name, bot_config):
    directory = bot_name
    script = bot_config.get("run")
    env_vars = bot_config.get("env", {})

    # Set environment variables
    print(f"Setting environment variables for {bot_name}")
    string_env_vars = {key: str(value) for key, value in env_vars.items()}  # Convert all values to strings
    os.environ.update(string_env_vars)

    # Start the bot
    print(f"Starting {bot_name} from {directory}/{script}")
    os.chdir(directory)
    process = subprocess.Popen(["python3", script], env=os.environ)
    os.chdir("..")
    return process

def main():
    processes = []

    for bot_name, bot_config in config.items():
        # Build each bot
        build_bot(bot_name, bot_config)

    print("Build process completed successfully.\n")

    for bot_name, bot_config in config.items():
        # Run each bot
        process = run_bot(bot_name, bot_config)
        processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        process.wait()

    print("""
    ███╗░░░███╗██████╗░  ██╗░░██╗░█████╗░██╗░░░░░██╗███████╗
    ████╗░████║██╔══██╗  ██║░██╔╝██╔══██╗██║░░░░░██║╚════██║
    ██╔████╔██║██████╔╝  █████═╝░███████║██║░░░░░██║░░░░██╔╝
    ██║╚██╔╝██║██╔══██╗  ██╔═██╗░██╔══██║██║░░░░░██║░░░██╔╝░
    ██║░╚═╝░██║██║░░██║  ██║░╚██╗██║░░██║███████╗██║░░██╔╝░░
    ╚═╝░░░░░╚═╝╚═╝░░╚═╝  ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░
    """)

if __name__ == "__main__":
    main()
