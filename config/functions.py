# --- Imports ---
import re, sys
from config.variables import LINE

# --- Repo validating function ---
def validateRepo(repo):
    repo = repo.strip().encode().decode('unicode_escape')

    # --- 1. Full HTTPS URL pattern ---
    httpsPattern = re.compile(
        r"^https://github\.com/[\w.-]+/[\w.-]+(?:/tree/[\w./-]+)?(?:\.git)?$"
    )

    # --- 2. SSH Git URL pattern ---
    sshPattern = re.compile(
        r"^git@github\.com:[\w.-]+/[\w.-]+(?:\.git)?$"
    )

    # --- 3. GitHub shorthand like user/repo[/tree/...] ---
    shorthandPattern = re.compile(
        r"^[\w.-]+/[\w.-]+(?:/tree/[\w./-]+)?$"
    )

    # --- Match checks ---

    if httpsPattern.match(repo) or sshPattern.match(repo):
        return repo

    if shorthandPattern.match(repo):
        return f"https://github.com/{repo}"

    sys.exit(f"Invalid repo format: '{repo}'. Must be a valid GitHub repository url or user/repo path.\n{LINE}")

# --- Validating amount commits type check function ---
def validateN(n):
    if type(n) == int and n > 0:
        return n
    else:
        return int(5)

# --- Validating output file function ---
def validateOutput(output):
    output = output.strip().lower().replace(" ", "-")

    output = re.sub(r"[^a-z0-9._-]", "", output)

    if not output.endswith(".json"):
        output += ".json"

    if not output or output in {".json", "-", "_"}:
        output = "report.json"

    return output