import json
import subprocess
import os

CONFIG_FILE = "bots_config.json"

def run_command(command, error_message):
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"{error_message}: {process.stderr}")
        exit(1)
    print(process.stdout)

if not os.path.exists(CONFIG_FILE):
    print(f"Configuration file {CONFIG_FILE} not found!")
    exit(1)

with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

for bot_name, bot_config in config.items():
    source = bot_config.get("source")
    branch = bot_config.get("branch", "main")
    script = bot_config.get("run")
    directory = bot_name

    if not source or not script:
        print(f"Missing 'source' or 'run' configuration for {bot_name}. Skipping.")
        continue

    if not os.path.isdir(directory):
        print(f"Cloning {bot_name} from {source} into {directory}")
        clone_command = f"git clone --branch {branch} {source} {directory}"
        run_command(clone_command, f"Failed to clone {source}")
    else:
        print(f"Directory {directory} already exists. Pulling latest changes.")
        pull_command = f"cd {directory} && git pull"
        run_command(pull_command, f"Failed to pull latest changes for {directory}")

    print(f"Installing dependencies for {bot_name}")
    requirements_file = os.path.join(directory, "requirements.txt")
    if os.path.exists(requirements_file):
        install_command = f"cd {directory} && pip3 install -r requirements.txt"
        run_command(install_command, f"Failed to install dependencies for {bot_name}")
    else:
        print(f"No requirements.txt found in {directory}. Skipping dependency installation.")

print("Build process completed successfully.")
print("""
███╗░░░███╗██████╗░      ██╗░░██╗░█████╗░██╗░░░░░██╗███████╗
████╗░████║██╔══██╗      ██║░██╔╝██╔══██╗██║░░░░░██║╚════██║
██╔████╔██║██████╔╝      █████═╝░███████║██║░░░░░██║░░░░██╔╝
██║╚██╔╝██║██╔══██╗      ██╔═██╗░██╔══██║██║░░░░░██║░░░██╔╝░
██║░╚═╝░██║██║░░██║      ██║░╚██╗██║░░██║███████╗██║░░██╔╝░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝      ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░
""")
