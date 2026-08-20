import logging
import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

logging.basicConfig(
    level = logging.INFO, # switch to DEBUG when needed
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError('Token not found in .env. Check if the file exists and token is correct.')

url = 'https://api.github.com/repos/pandas-dev/pandas/pulls?per_page=100&state=all&sort=updated&direction=desc'
headers = { 
    'Authorization': f'Bearer {token}'
}

# PR extraction
results = []
page_counter = 0
now = datetime.now(timezone.utc)
cutoff_date = now - timedelta(days=365) # 1 year ago
done = False
while url:
    response = requests.get(url, headers=headers)
    logger.debug(response.url)
    if response.status_code != 200:
        logger.error('Status Code: %d', response.status_code)
        break
    page_data = response.json()
    for pr in page_data:
        recent_pr_update_time = datetime.fromisoformat(pr['updated_at'])
        if recent_pr_update_time > cutoff_date:
            results.append(pr)
        else:
            done = True
            break
    if done:
        break
    page_counter += 1
    logger.info('Fetched page %d. Total PRs at: %d. Updated at: %s', page_counter, len(results), page_data[-1]['updated_at'])
    if 'next' in response.links:
        url = response.links['next']['url']
    else:
        url = None
logger.info('Fetched %d PRs', len(results))


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

logger.info('Transformed %d Slim PRs', len(slim_prs))
logger.debug(slim_prs[0])

