# --- Constants ---
LINE = "\n=========================================\n"

# --- Variables ---
gitRepo = str()
amountCommits = int(0)
outputFile = str()
repoCloned = bool(False)
tempDir = None
MODEL_REPO = "tensorblock/gpt4all-falcon-GGUF"
LLM_FILE_NAME = "gpt4all-falcon-Q5_K_M.gguf"

# --- Analysis Variables ---
repo = None
commits = list()
diffs = list()
llmResults = list()
llmPath = None