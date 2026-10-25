import requests
import json

with open(r"D:\Projects\linkedin-agent-studio\linkedin_user_data\session_cookies.json") as f:
    cookies_list = json.load(f)

cookies = {c["name"]: c["value"].strip('"').strip("'") for c in cookies_list}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "csrf-token": cookies.get("JSESSIONID", ""),
    "x-restli-protocol-version": "2.0.0"
}

res = requests.get("https://www.linkedin.com/voyager/api/me", cookies=cookies, headers=headers)
print("Voyager API Status:", res.status_code)
if res.status_code == 200:
    data = res.json()
    first = data.get("miniProfile", {}).get("firstName", "")
    last = data.get("miniProfile", {}).get("lastName", "")
    print(f"Logged in user verified: {first} {last}")
else:
    print("Response text:", res.text[:200])
