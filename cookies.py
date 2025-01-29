import json

with open("raw_cookies.json", "r") as f:
    raw_cookies = json.load(f)

cookies = {}
for cookie in raw_cookies:
    cookies[cookie["name"]] = cookie["value"]

with open("cookies.json", "w") as f:
    json.dump(cookies, f)
