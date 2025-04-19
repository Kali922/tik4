import json
import subprocess
import os
import time  # Import the time module
import threading

CONFIG_FILE = "bots_config.json"

def log_output(bot_name, process):
    """Logs the output of a bot's process in real-time."""
    while True:
        output = process.stdout.readline()
        if output:
            print(f"[{bot_name}] {output.strip()}")
        if process.poll() is not None:
            break
    stderr_output = process.stderr.read()
    if stderr_output:
        print(f"[{bot_name}] STDERR: {stderr_output.strip()}")

if not os.path.exists(CONFIG_FILE):
    print(f"Configuration file {CONFIG_FILE} not found!")
    exit(1)

with open(CONFIG_FILE, 'r') as f:
    config = json.load(f)

processes = []
threads = []

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
    process = subprocess.Popen(command, cwd=directory, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
    processes.append((bot_name, process))

    # Create a thread to log the output of this bot
    log_thread = threading.Thread(target=log_output, args=(bot_name, process))
    threads.append(log_thread)
    log_thread.daemon = True  # Allow the main script to exit even if the thread is running
    log_thread.start()

print("All bots are running and logging in the background.")
print("""
███╗░░░███╗██████╗░      ██╗░░██╗░█████╗░██╗░░░░░██╗███████╗
████╗░████║██╔══██╗      ██║░██╔╝██╔══██╗██║░░░░░██║╚════██║
██╔████╔██║██████╔╝      █████═╝░███████║██║░░░░░██║░░░░██╔╝
██║╚██╔╝██║██╔══██╗      ██╔═██╗░██╔══██║██║░░░░░██║░░░██╔╝░
██║░╚═╝░██║██║░░██║      ██║░╚██╗██║░░██║███████╗██║░░██╔╝░░
╚═╝░░░░░╚═╝╚═╝░░╚═╝      ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░
""")

# Keep the main script alive to continue logging
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping all bot loggers...")
    # No need to explicitly terminate bots here, as their output streams will close
    # when the bot processes themselves are terminated (usually by Ctrl+C in the bot's terminal).
    print("Loggers stopped.")
