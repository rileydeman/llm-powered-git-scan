# --- Python Version Check ---
import pprint
from os.path import exists

from config.version import checkPyVersion
checkPyVersion()

# --- Packages Check ---
from config.packages import checkPackages
checkPackages()

# --- Imports ---
import argparse, json, os, shutil, tempfile, tqdm, time, sys, warnings

from config.variables import *
from config.functions import validateRepo, validateN, validateOutput, isGitRepo
from git import Repo
from git.exc import GitCommandError
from dotenv import load_dotenv
from openai import OpenAI


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
    pbarTotal = 4

    print(f"\nStarting with analyzing commit diffs for sensitive data...\n")

    pbar = tqdm.tqdm(total=pbarTotal, desc="Analyzing commit diffs", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]")

    # 1. Get Commits from repo
    if repoCloned:
        repo = Repo(tempDir)
    else:
        repo = Repo(tempDir)

    commits = list(repo.iter_commits("HEAD", max_count=amountCommits))

    pbar.update(1)

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
                    "line": line[1:].strip(),
                    "type": "added"
                })
            elif line.startswith('-') and not line.startswith('---'):
                diffs.append({
                    "commit": commit.hexsha,
                    "file": currentFile,
                    "line": line[1:].strip(),
                    "type": "removed"
                })

    pbar.total += 3 * len(diffs)
    pbar.refresh()
    pbar.update(1)

    # 3. Scanning data for sensitive data

    # 3.1. Making batches for the LLM
    diffBatches = list()

    if len(diffs) <= 20:
        diffBatches.append(diffs)
        pbar.update(len(diffs))
    else:
        currentDiffIndex = 0
        currentBatch = 0
        inCurrentBatch = 0

        for diff in diffs:
            if len(diffBatches) <= currentBatch:
                diffBatches.append([])

            diffBatches[currentBatch].append(diff)
            inCurrentBatch += 1

            if inCurrentBatch == 20:
                currentBatch += 1
                inCurrentBatch = 0

            pbar.update(1)

    pbar.total += len(diffBatches)
    pbar.refresh()

    # 3.2. Analyzing with LLM
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        sys.exit("OPENAI_API_KEY not set, please set it in the .env file!")

    client = OpenAI(api_key=api_key)

    for batch in diffBatches:
        diffBlock = ""

        for i, diff in enumerate(batch):
            diffBlock += f"""
            DIFF #{i+1}
            Commit: {diff["commit"]}
            File: {diff["file"]}
            Modified line:
            {diff["line"]}
            ---
            """

        prompt = f"""
        You are a professional security auditor analyzing Git commit diffs for potential secrets or sensitive data.
        
        Analyze each DIFF separately and return a **single valid JSON array** with one object per DIFF:
        {{
            "diff_line": <the modified line>,
            "contains_sensitive_data": true/false,
            "confidence": <integer 0-100, the amount of percentage that you are confident of the findings>,
            "reason": "<short explanation>"
        }}
        
        Return **only JSON** with the object items in it, nothing else.
        {diffBlock}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a JSON-only security analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        output = json.loads(response.choices[0].message.content)

        if output["results"]:
            llmResults.append(output["results"])
        else:
            llmResults.append(output)

        pbar.update(1)

    pbar.update(1)

    # 4. Rewriting arrays for response
    for i, diff in enumerate(diffs):

        for batch in llmResults:
            for item in batch:
                if diff["line"] == item["diff_line"]:
                    diffs[i]["result"] = {
                        "contains_sensitive_data": item["contains_sensitive_data"],
                        "confidence": item["confidence"],
                        "reason": item["reason"]
                    }

        pbar.update(1)

    results = {
        "repo": gitRepo,
        "amount_commits_scanned": amountCommits - 1,
        "foundings": {}
    }

    for diff in diffs:
        if diff["result"]["contains_sensitive_data"]:
            item = {
                "type": diff["type"],
                "line": diff["line"],
                "file": diff["file"],
                "result": diff["result"]
            }
            results["foundings"].setdefault(diff["commit"], [])
            results["foundings"][diff["commit"]].append(item)

        pbar.update(1)

    pbar.update(1)

    pprint.pprint(results)
    pbar.close()