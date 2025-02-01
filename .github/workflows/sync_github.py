
import requests
import base64

GITHUB_TOKEN = "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"
GITHUB_REPO = "erfan1994/hiddify"
FILE_PATH = "Behnam_AJB_city"
BRANCH = "main"

# دانلود آخرین فایل
url = "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY_RAW.txt"
response = requests.get(url)

if response.status_code == 200:
    new_content = base64.b64encode(response.text.encode()).decode()
else:
    print("Failed to fetch file.")
    exit()

# دریافت SHA آخرین نسخه فایل
api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
response = requests.get(api_url, headers=headers)
if response.status_code == 200:
    sha = response.json()["sha"]
else:
    print("Failed to get file info.")
    exit()

# به‌روزرسانی فایل در GitHub
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
