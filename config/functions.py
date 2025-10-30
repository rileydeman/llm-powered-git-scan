# --- Imports ---
import re, sys, os
from config.variables import *
from git import Repo, InvalidGitRepositoryError, NoSuchPathError

# --- Repo validating function ---
def validateRepo(repo):
    repo = repo.strip()

    # --- 1. HTTPS Git URL (any domain) ---
    httpsPattern = re.compile(
        r"^https://[\w.-]+(?:/[\w./-]+)*\.git$"
    )

    # --- 2. SSH Git URL (any domain) ---
    sshPattern = re.compile(
        r"^(git|ssh)@[\w.-]+:[\w./-]+\.git$"
    )

    # --- 3. Local or relative repo path ---
    if os.path.exists(repo):
        abs_path = os.path.abspath(repo)
        # print(f"Detected local repository: {abs_path}")
        return abs_path

    # --- 4. HTTPS or SSH remote Git URLs ---
    if httpsPattern.match(repo) or sshPattern.match(repo):
        # print(f"Detected remote Git repository: {repo}")
        return repo

    # --- 5. GitHub shorthand like 'user/repo' (optional fallback) ---
    shorthandPattern = re.compile(r"^[\w.-]+/[\w.-]+$")
    if shorthandPattern.match(repo):
        url = f"https://github.com/{repo}.git"
        # print(f"Interpreting shorthand '{repo}' as {url}")
        return url

    # --- 6. Otherwise invalid ---
    sys.exit(f"Invalid repository format: '{repo}'.\nMust be a valid .git URL, SSH path, or local repo directory.")

# --- Validating amount commits type check function ---
def validateN(n):
    if type(n) == int and n > 0:
        return (n + 1)
    else:
        return int(6)

# --- Validating output file function ---
def validateOutput(output):
    output = output.strip().lower().replace(" ", "-")

    output = re.sub(r"[^a-z0-9._-]", "", output)

    if not output.endswith(".json"):
        output += ".json"

    if not output or output in {".json", "-", "_"}:
        output = "report.json"

    return output

# --- Is it a Git Repo check function ---
def isGitRepo(repo):
    try:
        _ = Repo(repo)
        return True
    except (InvalidGitRepositoryError, NoSuchPathError):
        print(f"Given path isn't a git repository: {repo}\n{LINE}")
        return False