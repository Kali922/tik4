import subprocess
import os

# For Linux (Debian/Ubuntu/Kali)
os.system("sudo apt update && sudo apt install -y git")

# OR for Windows
# os.system("choco install git -y")

# OR for macOS
# os.system("brew install git")


def run_command(command, wait=True):
    """Run a shell command and stream output live."""
    process = subprocess.Popen(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    if wait:
        for line in iter(process.stdout.readline, ""):
            print(line, end="")
        process.stdout.close()
        process.wait()
    else:
        print(f"[Started] {command} (logs will follow below)\n")
        for line in iter(process.stdout.readline, ""):
            print(line, end="")

if __name__ == "__main__":
    print("=== Building Bots... ===")
    run_command("python build_bots.py", wait=True)

    print("\n=== Running Bots... ===")
    run_command("python run_bots.py", wait=False)  # keeps running and logs live
