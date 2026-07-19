import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError('Token not found in .env. Check if the file exists and token is correct.')

#---

url = 'https://api.github.com/repos/pandas-dev/pandas/pulls?per_page=100&state=all'
headers = { 
    'Authorization': f'Bearer {token}'
}

results = []
page_counter = 0
while url:
    if page_counter == 5:
        break
    response = requests.get(url, headers=headers)
    print(response.url)
    if response.status_code != 200:
        print(f'Status Code: {response.status_code}')
        break
    page_data = response.json()
    results.extend(page_data)
    page_counter += 1
    print(page_counter)
    if 'next' in response.links:
        url = response.links['next']['url']
    else:
        url = None
print(len(results))
        