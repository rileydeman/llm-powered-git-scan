# --- Imports ---
import sys, urllib.request, re, webbrowser
from config.variables import LINE

correctVersion = False

def checkPyVersion():
    global correctVersion

    print("Checking python version...\n")

    if sys.version_info.major == 3 and sys.version_info.minor >= 10:
        correctVersion = True
    else:
        updatePython()

    if correctVersion:
        print(f"You are on a supported Python version ({sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})\n{LINE}")


def updatePython():
    print(f"Your Python version is outdated. Required 3.10.0 or higher, your version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}.\n")

    latest_version = getLatestPythonVersion()
    print(f"Latest version available: {latest_version}")

    download_link = f"https://www.python.org/ftp/python/{latest_version}/python-{latest_version}-amd64.exe"
    print(f"Download it here:\n{download_link}\n")
    try:
        webbrowser.open(download_link)
        print("The download page has been opened in your default browser.\n")
    except Exception:
        print("Could not open the browser automatically.\n")

    sys.exit(f"Please install the latest Python version manually, then restart this program.\n{LINE}")


def getLatestPythonVersion():
    print("Fetching latest Python version info...")
    try:
        with urllib.request.urlopen("https://www.python.org/downloads/") as response:
            raw = response.read()
            try:
                html = raw.decode("utf-8")
            except UnicodeDecodeError:
                html = raw.decode("latin-1")

        match = re.search(r"Python (\d+\.\d+\.\d+)", html)
        if match:
            version = match.group(1)
            print(f"Latest version detected: {version}\n")
            return version
        else:
            print("Could not detect version automatically, using fallback 3.14.0.\n")
            return "3.14.0"
    except Exception as e:
        print(f"Error checking version: {e}\n")
        return "3.14.0"
