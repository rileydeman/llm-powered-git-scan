# --- Imports ---
import importlib.util, subprocess, sys
from config.variables import *

# --- Variables ---
checkedForPackages = int(0)
packages = [
    {
        "name": "git",
        "installed": bool(False)
    },
    {
        "name": "tqdm",
        "installed": bool(False)
    },
    {
        "name": "gpt4all",
        "installed": bool(False)
    },
    {
        "name": "huggingface_hub",
        "installed": bool(False)
    }
]

# --- Package Checker function ---
def checkPackages():
    global checkedForPackages, packages
    reRunFunction = bool(False)

    print("Checking packages...\n")

    for pkg in packages:
        if checkedForPackages == 0 or not pkg["installed"]:
            spec = importlib.util.find_spec(pkg["name"])

            if spec is None:
                print(f"{pkg['name']} is not installed! Installing...")
                reRunFunction = True

                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg["name"]])
            else:
                pkg["installed"] = True

                if checkedForPackages == 0:
                    print(f"{pkg['name']} is already installed!")
                else:
                    print(f"{pkg['name']} is installed!")

    checkedForPackages += 1
    if reRunFunction:
        print("Re-running packages check...")

        if checkedForPackages < 5:
            checkPackages()
        else:
            sys.exit(f"\nThere went something wrong, the program has been aborted!\n{LINE}")
    else:
        print(f"\nAll packages are available!\n{LINE}")