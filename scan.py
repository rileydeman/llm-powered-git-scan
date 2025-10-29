# --- Python Version Check ---
from config.version import checkPyVersion
checkPyVersion()

# --- Packages Check ---
from config.packages import checkPackages
checkPackages()

# --- Imports ---
import argparse, os
from config.variables import *
from config.functions import validateRepo, validateN, validateOutput, isGitRepo
from git import Repo

# --- Set parser arguments ---
parser = argparse.ArgumentParser()
parser.add_argument("--repo", "--r", type=str, required=True, help="Specify git repository url or path")
parser.add_argument("--n", type=int, required=True, help="Specify the amount of commits you want to scan")
parser.add_argument("--out", "--o", type=str, default="report.json", required=False, help="Specify the output file (default is report.json)")

# --- Retrieve parser arguments values ---
args = parser.parse_args()

gitRepo = validateRepo(args.repo)
amountCommits = validateN(args.n)
outputFile = validateOutput(args.out)

# --- Main program ---
if len(gitRepo) > 1 and amountCommits > 0 and len(outputFile) > 1:
    print("Checking location of given Git Repo...\n")

    if os.path.isdir(gitRepo) and isGitRepo(gitRepo):
        print(f"Local Repo Detected: {gitRepo}\n{LINE}")
    elif gitRepo.endswith(".git"):
        print(f"External Repo Detected: {gitRepo}\n")