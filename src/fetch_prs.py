import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError('Token not found in .env. Check if the file exists and token is correct.')

#---

url = 'https://api.github.com/repos/pandas-dev/pandas/pulls?per_page=100&state=all&sort=updated&direction=desc'
headers = { 
    'Authorization': f'Bearer {token}'
}

results = []
page_counter = 0
now = datetime.now(timezone.utc)
cutoff_date = now - timedelta(days=365) # 1 year ago
done = False
while url:
    response = requests.get(url, headers=headers)
    #print(response.url)
    if response.status_code != 200:
        print(f'Status Code: {response.status_code}')
        break
    page_data = response.json()
    for pr in page_data:
        recent_pr_update_time = datetime.fromisoformat(pr['updated_at'])
        if recent_pr_update_time > cutoff_date:
            results.append(pr)
        elif recent_pr_update_time < cutoff_date:
            done = True
            break
    if done:
        break
    page_counter += 1
    #print(page_counter)
    if 'next' in response.links:
        url = response.links['next']['url']
    else:
        url = None
print(len(results))


# slim dict loop for desired fields
slim_prs = []
for pr in results:
    slim_pr = {
        'id' : pr['id'],
        'number' : pr['number'],
        'user_login' : pr['user']['login'],
        'user_type' : pr['user']['type'],
        'created_at' : pr['created_at'],
        'merged_at' : pr['merged_at'],
        'closed_at' : pr['closed_at'],
        'updated_at' : pr['updated_at'],
        'labels' : [label['name'] for label in pr['labels']],
        'state' : pr['state'],
        'title' : pr['title'],
        'draft' : pr['draft']
    }
    slim_prs.append(slim_pr)

print(len(slim_prs))
print(slim_prs[0])

