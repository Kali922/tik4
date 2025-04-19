import json
import subprocess
import os
from dotenv import dotenv_values

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

    print(f"Setting environment variables for {bot_name}")
    os.environ.update(env_vars)

    print(f"Starting {bot_name} from {os.path.join(directory, script)}")
    command = f"python3 {script}"
    process = subprocess.Popen(command, cwd=directory, shell=True)
    processes.append((bot_name, process))

print("All bots are running in the background.")
print("""
███╗░░░███╗██████╗░      ██╗░░██╗░█████╗░██╗░░░░░██╗███████╗
████╗░████║██╔══██╗      ██║░██╔╝██╔══██╗██║░░░░░██║╚════██║
██╔████╔██║██████╔╝      █████═╝░███████║██║░░░░░██║░░░░██╔╝
██║╚██╔╝██║██╔══██╗      ██╔═██╗░██╔══██║██║░░░░░██║░░░██╔╝░
██║░╚═╝░██║██║░░██║      ██║░╚██╗██║░░██║███████╗██║░░██╔╝░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝      ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░
""")

# Optionally, you can add a loop to keep the main script running
# and potentially monitor the child processes.
# For now, we'll just let them run in the background.
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping all bots...")
    for name, proc in processes:
        print(f"Terminating {name} (PID: {proc.pid})...")
        proc.terminate()
    for name, proc in processes:
        proc.wait()
    print("All bots stopped.")
