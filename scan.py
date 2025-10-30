# --- Python Version Check ---
from config.version import checkPyVersion
checkPyVersion()

# --- Packages Check ---
from config.packages import checkPackages
checkPackages()

# --- Imports ---
import argparse, json, os, shutil, tempfile, tqdm, time, sys, io, warnings

from config.variables import *
from config.functions import validateRepo, validateN, validateOutput, isGitRepo
from git import Repo
from git.exc import GitCommandError
from huggingface_hub import hf_hub_download
from gpt4all import GPT4All

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
warnings.filterwarnings("ignore", message=r".*Failed to load llamamodel.*", category=UserWarning)

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


    # --- Analyzing Commits ---
    pbarTotal = 3

    print(f"\nStarting with analyzing commit diffs for sensitive data...")

    if not os.path.exists(f"llm/{LLM_FILE_NAME}"):
        print(f"LLM file not found, analyse may take 5 to 15 minutes longer due to extra installation (from around 5.7GB).\n")
        pbarTotal += 5
    else:
        print("\n")

    pbar = tqdm.tqdm(total=pbarTotal, desc="Analyzing commit diffs", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]")

    # 1. Get Commits from repo
    if repoCloned:
        repo = Repo(tempDir)
    else:
        repo = Repo(tempDir)

    commits = list(repo.iter_commits("HEAD", max_count=amountCommits))

    pbar.update(1)

    # print(commits)

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
            if line.startswith("+++ b/"):
                currentFile = line[6:].strip()

            if line.startswith("+") and not line.startswith("+++"):
                diffs.append({
                    "commit": commit.hexsha,
                    "file": currentFile,
                    "line": line[1:].strip()
                })

    pbar.total += len(diffs)
    pbar.refresh()
    pbar.update(1)

    # print(diffs)

    # 3. Scanning data for sensitive data

    # 3.1. Downloading LLM file (if needed)
    baseDir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(f"llm/{LLM_FILE_NAME}"):
        llmDir = os.path.join(baseDir, "llm")

        if not os.path.exists(llmDir):
            os.mkdir(llmDir)

        llmPath = hf_hub_download(
            repo_id=MODEL_REPO,
            filename=LLM_FILE_NAME,
            cache_dir=llmDir,
        )

        shutil.copyfile(llmPath, os.path.join(llmDir, LLM_FILE_NAME))
        shutil.rmtree(f"{llmDir}/.locks")
        shutil.rmtree(f"{llmDir}/models--tensorblock--gpt4all-falcon-GGUF")

        pbar.update(5)

    # 3.2 Analyzing with LLM
    model = GPT4All(model_name=f"{baseDir}/llm/{LLM_FILE_NAME}")

    for diff in diffs:
        commitHash = diff["commit"]
        diffText = diff["line"]
        filePath = diff["file"]
        result = None

        prompt = f"""
        You are a professional security auditor that checks code changes for secrets or sensitive data.

        Below is a single line of modified code from a Git commit.
        Your task is to determine if it contains sensitive information.

        ---
        Commit: {commitHash}
        File: {filePath}
        Modified line:
        {diffText}
        ---

        Return your analysis ONLY as a **single JSON object** with no commentary or explanation.
        Use this exact schema, and fill in actual values (so replace only the text in the brackets including the brackets):
        {{
          "contains_sensitive_data": (your input in only true or false),
          "confidence": (your input in only a number between 0 and 100),
          "reason": "(your input in text as your explanation)"
        }}
        """

        print(diffText)
        output = model.generate(prompt, max_tokens=512, temp=0.1)

        try:
            result = json.loads(output)
        except json.decoder.JSONDecodeError:
            result = {
                "contains_sensitive_data": False,
                "confidence": 0,
                "reason": "Failed to parse LLM response"
            }

        print(result)

        pbar.update(1)

    pbar.update(1)
    pbar.close()