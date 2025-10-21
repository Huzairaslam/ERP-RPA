import requests

url = "https://hooks.slack.com/services/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"
payload = {
    "text": "🚀 Test alert: Slack webhook is working!",
}
response = requests.post(url, json=payload)

print("Status:", response.status_code)
print("Response:", response.text)
