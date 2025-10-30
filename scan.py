# --- Python Version Check ---
from config.version import checkPyVersion
checkPyVersion()

# --- Packages Check ---
from config.packages import checkPackages
checkPackages()

# --- Imports ---
import argparse, gpt4all, json, os, shutil, tempfile, tqdm, time
from config.variables import *
from config.functions import validateRepo, validateN, validateOutput, isGitRepo
from git import Repo
from git.exc import GitCommandError

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
        print(f"External Repo Detected: {gitRepo}\nRequired cloning, progress starts now...\n")

        # Cloning the external repo to the device
        pbar = tqdm.tqdm(total=3, desc="Cloning Git Repo", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]")

        tempDir = tempfile.mkdtemp(prefix="gitscan-") # Making a temporary folder
        time.sleep(1)
        pbar.update(1)
        Repo.clone_from(gitRepo, tempDir, depth=amountCommits) # Cloning the repository
        pbar.update(1)
        repoCloned = True # Switching the repoCloned var to True
        time.sleep(1)
        pbar.update(1)
        pbar.close()

        print(f"\nRepo successfully cloned!\n{LINE}")


    # --- Analysing Commits ---

    # 1. Get Commits from repo
    if repoCloned:
        repo = Repo(tempDir)
    else:
        repo = Repo(tempDir)

    commits = list(repo.iter_commits("HEAD", max_count=amountCommits))

    print(commits)

    # 2. Get diffs from commits
    for commit in commits:
        if not commit.parents:
            continue

        parent = commit.parents[0]

        try:
            diff_text = repo.git.diff(parent.hexsha, commit.hexsha)
        except GitCommandError:
            continue

        for line in diff_text.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                diffs.append({
                    "commit": commit.hexsha,
                    "file": None,
                    "line": line[1:].strip()
                })

    print(diffs)