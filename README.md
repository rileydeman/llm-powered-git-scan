# LLM Powered Git Scan

![Built with Python](https://img.shields.io/badge/built_with-Python-blue?logo=python)
![Python Version](https://img.shields.io/badge/python-3.14%2B-blue)
![Version](https://img.shields.io/badge/version-1.0.0-success)
![License](https://img.shields.io/badge/license-Custom-lightgrey)
![Status](https://img.shields.io/badge/status-Stable-brightgreen)
![Contributions](https://img.shields.io/badge/contributions-closed-red)

An LLM powered git scan who searched in an x number of latest commits on a git repo for secrets and other sensitive data.

Note: This is an assignment to from JetBrains for an internship position.

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Installation](#-installation)
- [Usage](#-usage)
- [Technical Information](#-technical-information)
- [Troubleshooting](#-troubleshooting)
- [License Notice](#-license-notice)
- [Copyright](#-copyright)
- [License](#-license)

---

## 🧩 Overview

`llm-powered-git-scan` is an **AI-assisted Git repository scanner** that analyzes commit diffs for potential **secrets**, **API keys**, or other **sensitive data** using the **OpenAI API**.

The tool clones or scans a given Git repository, iterates through recent commits, and sends code diffs to an LLM (like **GPT-4o-mini** or **GPT-5-mini**) for intelligent, context-aware security analysis.

It detects sensitive code patterns that traditional regex scanners often miss — such as access tokens, credentials, or embedded API keys — and generates a structured JSON report for auditing and review.

### **Core Features**
- 🤖 AI-powered detection of sensitive data and secrets.
- 🧠 Uses **OpenAI GPT models** (no local inference required).
- 📦 Automatically installs missing dependencies.
- 💾 Outputs detailed JSON reports to your Documents folder.
- 🪶 Works on **Windows, macOS, and Linux**.
- 🔍 Scans both **local** and **remote (GitHub)** repositories.

### **Use case example**
> You provide a GitHub repo URL or local path.  
> The program clones or reads it, analyzes recent commits using an LLM, and saves a clean JSON report showing which code lines might expose secrets.

---

## ⚙️ Installation

Follow these steps to install and run **gitscan**:

1. **Download the latest release**
   - Go to the [Releases](https://github.com/rileydeman/llm-powered-git-scan/releases) page.
   - Under **Assets**, download the file named **Source code (zip)**.
   - This will download a file such as `llm-powered-git-scan-1.0.0.zip`.

2. **Extract the files**
   - Right-click the ZIP file → **Extract All...**
   - Choose a simple folder path, for example:  
     `C:\gitscan`

3. **Open Command Prompt in that folder**
   - Open the folder where you extracted the project.  
   - Click on the **address bar** in File Explorer (the path at the top).  
   - Type `cmd` and press **Enter** — this will open Command Prompt directly in that folder.

4. **Add your OpenAI API key**
   - In the extracted folder, locate the file named `example.env`.  
   - Rename it to `.env`  
   - Open it with a text editor (like Notepad) and enter your API key:
     ```
     OPENAI_API_KEY=sk-YOUR-API-KEY
     ```
   - Save and close the file.

5. **Run the program**
   Depending on your Python setup, one of the following commands will start the program:

   **Option 1 (most common):**
   ```bash
   python scan.py --repo "<repo_url_or_local_path>" --n <commit_count> --out "<output_name>.json"

   Option 2:
    ```bash
   py scan.py --repo "<repo_url_or_local_path>" --n <commit_count> --out "<output_name>.json"
    ```
   Example:
    ```bash
   python scan.py --repo "https://github.com/example/project.git" --n 10 --out "scan_results.json"
    ```
6. **First-time setup**
   - On your first run, the program will automatically:
     - Check for required Python packages (like `gitpython`, `tqdm`, `requests`, and `openai`).
     - Install any that are missing.
     - Restart itself automatically once installation is complete.

7. **Done!**
   - You’ll see progress bars showing:
     - Git cloning progress (if a remote repository is being scanned)
     - Commit analysis progress
   - Once finished, your scan report will be automatically saved to:
     ```
     Documents/gitscan/<output_name>.json
     ```

   Example:
    ```
   C:\Users<yourname>\Documents\gitscan\scan_results.json
   ```
   You can open the JSON file in any text editor or JSON viewer to review detected sensitive data findings.


### 🧹 Stopping the Scan
To stop the scan at any time, simply **close the Command Prompt window**.  
Temporary cloned repositories (for remote Git URLs) are automatically deleted after the scan completes.


---

## 💻 Usage

Once installed and configured, you can start scanning repositories directly from the command line.


### 🧩 Basic Command

```bash
py scan.py --repo "<repo_url_or_local_path>" --n <commit_count> --out "<output_name>.json"
```
<table>
<thead>
    <tr>
        <th>Argument</th>
        <th>Description</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>--repo</td>
        <td>The Git repository to scan. Accepts both local paths and remote URLs (e.g. https://github.com/user/repo.git).</td>
    </tr>
    <tr>
        <td>--n</td>
        <td>The number of recent commits to analyze.</td>
    </tr>
    <tr>
        <td>--out</td>
        <td>The name of the output JSON file that will be saved in your Documents/gitscan folder.</td>
    </tr>
</tbody>
</table>

---

### ⚙️ What Happens During a Scan
1. **Repository detection**
   - If the path points to a **local repository**, it’s analyzed directly.
   - If it’s a **remote GitHub URL**, the repository is cloned into a temporary folder.
2. **Commit extraction**
   - The last *N* commits are retrieved.
3. **Diff analysis**
   - Each code change (`+` and `-` lines) is sent to the **OpenAI GPT model** for inspection.
4. **LLM evaluation**
   - The model identifies potential secrets, credentials, or sensitive information.
5. **Report generation**
   - All findings are saved into a structured JSON report inside your `Documents/gitscan` folder.


### 🧾 Example Workflow

```bash
py scan.py --repo "https://github.com/org/app.git" --n 15 --out "report.json"
````
---

## 🧠 Technical Information

<table>
<thead>
    <tr>
        <th>Specification</th>
        <th>Description</th>
    </tr>
</thead>
<tbody>
    <tr>
        <td>Programming Languages</td>
        <td>Python</td>
    </tr>
    <tr>
        <td>Packages Used</td>
        <td>GitPython, tqdm, dotenv, openai</td>
    </tr>
    <tr>
        <td>APIs Used</td>
        <td>ChatGPT</td>
    </tr>
    <tr>
        <td>Deployment Target</td>
        <td>Windows, Linux & MacOS</td>
    </tr>
    <tr>
        <td>Primary Language</td>
        <td>English (en-AU)</td>
    </tr>
</tbody>
</table>

---

## 🧩 Troubleshooting

Having issues getting **gitscan** to run or generate reports correctly?  
Here are some common problems and their solutions:

### 🔹 The program closes instantly
- This usually happens if **Python** isn’t installed or isn’t added to your system PATH.  
- Check by running:
  ```bash
  python --version
    ```
  or
  ```bash
  py --version
    ```
- If the command isn’t recognized, [download Python](https://www.python.org/downloads/) and make sure to check **“Add Python to PATH”** during installation.
- You can also start the script manually to see error messages:
  ```bash
  py scan.py

### 🔹 “Missing API key” or “Invalid API key” error
- Make sure you have a `.env` file in the same folder as `scan.py`.
- The file must contain your valid OpenAI API key:
    ```dotenv
  OPENAI_API_KEY=sk-YOUR-API-KEY
    ```
- Double-check that:
  - There are **no spaces or extra characters** in the key.
  - You did not include quotes (`"`) around it.
  - Your API key is **active** and associated with your OpenAI account.

### 🔹 “Rate limit” or “Quota exceeded” errors
- This means your OpenAI API plan has temporarily hit its usage limit.
- Solutions:
- Wait a few minutes and try again.
- If you use the **free trial**, you might need to upgrade to a paid account.
- Reduce your commit count (`--n`) to scan fewer diffs per run to save tokens.

### 🔹 The scan is very slow
- Scanning time depends on:
  - The number of commits (`--n`).
  - The model used (e.g. `gpt-4o-mini` is faster than `gpt-5-mini`).
  - Your internet connection speed.
  - Tips to improve performance:
    - Reduce `--n` to scan fewer commits.
    - Use smaller repositories for testing.
    - Ensure no other heavy network tasks are running during the scan.

### 🔹 The JSON report is empty
If your output JSON file is empty or incomplete:
1. Make sure the repository actually contains recent commits with code changes.  
2. Verify that your `--n` value is not larger than the number of available commits.  
3. Check the console output — if you see parsing errors from the LLM, the model might have returned invalid JSON.  
4. Try running again with a lower number of commits or switching to a different model (`gpt-4o-mini` or `gpt-5-mini`).

### 🔹 Permission denied or file write errors
- This can happen if the program doesn’t have permission to write to your Documents folder.  
- Try running Command Prompt **as Administrator**, or specify a different output name (without special characters).  
- Ensure your user account has write access to the Documents folder, example:
    ```
  C:\Users\<yourname>\Documents\gitscan\
  ```

### 🔹 Temporary folder not deleted
- If the scan is interrupted before completion, the temporary cloned repository might not get removed automatically.
- You can safely delete it manually:
- On Windows:  
  ```
  %TEMP%\gitscan_tmp_*
  ```
- On macOS/Linux:  
  ```
  /tmp/gitscan_tmp_*
  ```

### 🔹 Seeing CUDA or GPU-related errors
- These messages can be safely ignored.  
- OpenAI’s GPT models run **in the cloud**, not on your local GPU — the program does not use CUDA or require a GPU.

### 🔹 Still not working?
If you’ve verified all the above steps and it’s still not working:
1. Close all terminal windows.
2. Reopen a new Command Prompt in your project folder.
3. Run:
    ```bash
    py scan.py --repo <repo_url_or_local_path> --n 5 --out "test.json"
    ```
4. Check the console output for detailed error information.

If issues persist, re-download the latest version from the [Releases](https://github.com/rileydeman/llm-powered-git-scan/releases) page to ensure you’re using the newest build.

---

## ⚠️ License Notice

This project is licensed for **personal and educational use only**.

- ✅ **Allowed:** Personal projects, private learning, classroom demonstrations, and student research.
- ❌ **Not allowed:** Public sharing, republishing, redistribution, or any form of commercial use.

To use this project (or any part of it) in a **public** or **commercial** context, you must obtain **written permission** from the author:

**Author:** [@rileydeman](https://github.com/rileydeman)

See the full [LICENSE](./LICENSE) file for complete terms and conditions.

---

## ©️ Copyright

All code and visual assets in this repository are &copy; rileydeman.

- Code is licensed for personal and educational use only.
- Logos, icons, and images are not open source and may not be reused without permission.

See the [LICENSE](./LICENSE) file for full terms.

---

## 📝 License

Custom license &copy; [rileydeman](https://github.com/rileydeman)  
See the [LICENSE](./LICENSE) file for full terms.

---

&copy; [rileydeman](https://www.rileydeman.com/)