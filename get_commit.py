import os
import requests
import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv(".env")

# --- Configuration ---
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
AI_API_KEY = os.getenv("AI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DAYS = 30  # commits from the last 7 days
client = Groq(api_key=AI_API_KEY)

# --- GitHub Commit Search ---
since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=DAYS)).date().isoformat()
url = f"https://api.github.com/search/commits?q=author:{GITHUB_USERNAME}+committer-date:>{since}"
headers = {
    "Accept": "application/vnd.github.cloak-preview+json",  # needed for commit search
    "Authorization": f"token {GITHUB_TOKEN}"
}


response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error {response.status_code}: {response.text}")
    exit()

data = response.json()

if not data.get("items"):
    print(f"No commits found in the last {DAYS} days.")
# else:
#     for commit in data["items"]:
#         repo = commit["repository"]["full_name"]
#         message = commit["commit"]["message"].split("\n")[0]
#         date = commit["commit"]["author"]["date"]
#         print(f"[{repo}] {date}\n→ {message}\n")

print(f"Total commits found: {len(data.get('items', []))}")


# --- AI Summary ---
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": f"Create a concise summary of the following GitHub commits made by the user {GITHUB_USERNAME} in the last {DAYS} days. Highlight key contributions and any notable patterns or themes in the commit messages. Here are the commits:\n" + "\n".join([f"- {commit['commit']['message']}" for commit in data.get("items", [])])
      },
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None 
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")