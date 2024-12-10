import requests

url = "http://localhost:8085/api/documents/"

payload = "<file contents here>"
headers = {
  'Accept': '*/*',
  'Content-Type': 'application/octet-stream'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
