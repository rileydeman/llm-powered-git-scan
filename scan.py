# --- Python Version Check ---
from config.version import checkPyVersion
checkPyVersion()

# --- Packages Check ---
from config.packages import checkPackages
checkPackages()

# --- Imports ---
from config.variables import *

print(f"Hello World!\n{LINE}")