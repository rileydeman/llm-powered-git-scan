# --- Python Version Check ---
from config.version import checkPyVersion
checkPyVersion()

# --- Packages Check ---
from config.packages import checkPackages
checkPackages()

# --- Imports ---
import argparse
from config.variables import *
from config.functions import validateRepo, validateN, validateOutput

## --- Set parser arguments ---
parser = argparse.ArgumentParser()
parser.add_argument("--repo", "--r", type=str, required=True, help="Specify the repository url or path")
parser.add_argument("--n", type=int, required=True, help="Specify the amount of commits you want to scan")
parser.add_argument("--out", "--o", type=str, default="report.json", required=False, help="Specify the output file (default is report.json)")

args = parser.parse_args()

print(args)

gitRepo = validateRepo(args.repo)
amountCommits = validateN(args.n)
outputFile = validateOutput(args.out)

print(f"Repo: {gitRepo}")
print(f"Commits: {amountCommits}")
print(f"Output File: {outputFile}")