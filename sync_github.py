import requests
import base64

GITHUB_TOKEN = "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"
GITHUB_REPO = "erfan1994/hiddify"
FILE_PATH = "Behnam_AJB_city"
BRANCH = "main"

# download lastest file
url = "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY_RAW.txt"
response = requests.get(url)

if response.status_code == 200:
    new_content = base64.b64encode(response.text.encode()).decode()
else:
    print("Failed to fetch file.")
    exit()

# receive last sha file
api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
response = requests.get(api_url, headers=headers)
if response.status_code == 200:
    sha = response.json()["sha"]
else:
    print("Failed to get file info.")
    exit()

# update file in Github
data = {
    "message": "Auto-update Behnam_AJB_city",
    "content": new_content,
    "sha": sha,
    "branch": BRANCH,
}

response = requests.put(api_url, json=data, headers=headers)

if response.status_code == 200:
    print("File updated successfully!")
else:
    print(f"Failed to update file: {response.json()}")
