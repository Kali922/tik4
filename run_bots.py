import json
import subprocess
import os

CONFIG_FILE = "bots_config.json"

if not os.path.exists(CONFIG_FILE):
    print(f"Configuration file {CONFIG_FILE} not found!")
    exit(1)

with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

processes = []

for bot_name, bot_config in config.items():
    script = bot_config.get("run")
    directory = bot_name
    env_vars = bot_config.get("env", {})

    if not script:
        print(f"Missing 'run' configuration for {bot_name}. Skipping.")
        continue

    print(f"\n--- Starting {bot_name} ---")

    # Set environment variables for the current bot
    os.environ.update(env_vars)

    command = f"python3 {script}"
    process = subprocess.Popen(command, cwd=directory, shell=True)
    processes.append((bot_name, process))

# Wait for all bots to finish
for bot_name, process in processes:
    process.wait()
    if process.returncode != 0:
        print(f"\n--- {bot_name} exited with code {process.returncode} ---")
    else:
        print(f"\n--- {bot_name} finished ---")

# Restore original environment variables (optional)
os.environ.clear()
print("\nAll bots have been executed.")
print("""
███╗░░░███╗██████╗░      ██╗░░██╗░█████╗░██╗░░░░░██╗███████╗
████╗░████║██╔══██╗      ██║░██╔╝██╔══██╗██║░░░░░██║╚════██║
██╔████╔██║██████╔╝      █████═╝░███████║██║░░░░░██║░░░░██╔╝
██║╚██╔╝██║██╔══██╗      ██╔═██╗░██╔══██║██║░░░░░██║░░░██╔╝░
██║░╚═╝░██║██║░░██║      ██║░╚██╗██║░░██║███████╗██║░░██╔╝░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝      ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░
""")
